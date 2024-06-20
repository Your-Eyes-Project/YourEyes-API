import numpy as np
import cv2 as cv
import math
from ultralytics import YOLO
from app.utils.shared_storage import storage
import app.proto.videostream_pb2 as videostream_pb2
import app.proto.videostream_pb2_grpc as videostream_pb2_grpc
import grpc

class VideoStreamerServicer(videostream_pb2_grpc.VideoStreamerServicer):
    def __init__(self, model):

        self.model = model  # Load the model only once during initialization
        self.frame_count = 0  # Initialize a frame counter
        self.class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train",
                            "truck", "boat",
                            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
                            "bird", "cat",
                            "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
                            "backpack", "umbrella",
                            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
                            "sports ball", "kite", "baseball bat",
                            "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
                            "wine glass", "cup",
                            "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich",
                            "orange", "broccoli",
                            "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
                            "pottedplant", "bed",
                            "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote",
                            "keyboard", "telephone",
                            "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock",
                            "vase", "scissors",
                            "teddy bear", "hair drier", "toothbrush"]
        self.object_dimensions = {
            "person": "0.50",
            "bicycle": "0.45",
            "car": "1.80",
            "motorbike": "0.90",
            "aeroplane": "4.00",
            "bus": "2.50",
            "train": "3.00",
            "truck": "2.50",
            "boat": "2.50",
            "traffic light": "0.30",
            "fire hydrant": "0.25",
            "stop sign": "0.60",
            "parking meter": "0.20",
            "bench": "1.50",
            "bird": "0.10",
            "cat": "0.45",
            "dog": "0.30",
            "horse": "0.50",
            "sheep": "0.45",
            "cow": "0.80",
            "elephant": "2.50",
            "bear": "1.00",
            "zebra": "0.50",
            "giraffe": "0.60",
            "backpack": "0.55",
            "umbrella": "0.50",
            "handbag": "0.40",
            "tie": "0.10",
            "suitcase": "0.45",
            "frisbee": "0.25",
            "skis": "0.10",
            "snowboard": "0.25",
            "sports ball": "0.22",
            "kite": "0.90",
            "baseball bat": "0.08",
            "baseball glove": "0.30",
            "skateboard": "0.20",
            "surfboard": "0.50",
            "tennis racket": "0.25",
            "bottle": "0.20",
            "wine glass": "0.25",
            "cup": "0.15",
            "fork": "0.15",
            "knife": "0.25",
            "spoon": "0.15",
            "bowl": "0.30",
            "banana": "0.20",
            "apple": "0.07",
            "sandwich": "0.20",
            "orange": "0.08",
            "broccoli": "0.20",
            "carrot": "0.05",
            "hot dog": "0.05",
            "pizza": "0.40",
            "donut": "0.10",
            "cake": "0.30",
            "chair": "0.50",
            "sofa": "2.00",
            "pottedplant": "0.50",
            "bed": "1.90",
            "diningtable": "1.00",
            "toilet": "0.60",
            "tvmonitor": "1.00",
            "laptop": "0.40",
            "mouse": "0.10",
            "remote": "0.20",
            "keyboard": "0.30",
            "telephone": "0.20",
            "microwave": "0.60",
            "oven": "0.60",
            "toaster": "0.30",
            "sink": "0.60",
            "refrigerator": "0.90",
            "book": "0.18",
            "clock": "0.30",
            "vase": "0.25",
            "scissors": "0.10",
            "teddy bear": "0.45",
            "hair drier": "0.15",
            "toothbrush": "0.16"
        }

    async def StreamVideo(self, request_iterator, context):

        async for video_frame in request_iterator:

            frame = self.decode_frame(video_frame)
            if frame is not None:
                self.frame_count += 1
                print(self.frame_count)
                if self.frame_count % 1 == 0:
                    detections = await self.run_model(frame)
                    await context.write(videostream_pb2.StreamStatus(
                        success=True,
                        message="Detections processed",
                        detections=detections
                    ))
            else:
                print("Failed to decode the frame.")

        # Send a final message indicating the end of the stream
        await context.write(videostream_pb2.StreamStatus(success=True, message="Stream completed"))

    async def run_model(self, frame):
        detections = []
        target_classes = storage.get_data('target_objects')
        if len(target_classes) == 0:
            target_classes = None
            print("No target objects configured.")
        results = self.model.predict(frame, classes=target_classes, conf=0.5, )
        frame_width = int(frame.shape[1])
        frame_height = int(frame.shape[0])

        NAMES = results[0].names
        for obj in results[0].boxes:

            target_object, real_width = self.width_calculation(NAMES[int(obj.cls[0])])

            x1, y1, x2, y2 = int(obj.xyxy[0][0]), int(obj.xyxy[0][1]), int(obj.xyxy[0][2]), int(
                obj.xyxy[0][3])

            camera_width = x2 - x1
            distance = (real_width * frame_width) / camera_width

            obj_center_x = (x1 + x2) // 2
            obj_center_y = (y1 + y2) // 2

            camera_middle_x = frame_width // 2
            camera_middle_y = frame_height // 2

            vector_x = obj_center_x - camera_middle_x
            vector_y = obj_center_y - camera_middle_y

            angle_deg = math.degrees(math.atan2(vector_y, vector_x))

            if angle_deg < 0:
                angle_deg += 360

            if 0 <= angle_deg < 30:
                direction = "3 o'clock"
            elif 30 <= angle_deg < 60:
                direction = "2 o'clock"
            elif 60 <= angle_deg < 90:
                direction = "1 o'clock"
            elif 90 <= angle_deg < 120:
                direction = "12 o'clock"
            elif 120 <= angle_deg < 150:
                direction = "11 o'clock"
            elif 150 <= angle_deg < 180:
                direction = "10 o'clock"
            elif 180 <= angle_deg < 210:
                direction = "9 o'clock"
            elif 210 <= angle_deg < 240:
                direction = "8 o'clock"
            elif 240 <= angle_deg < 270:
                direction = "7 o'clock"
            elif 270 <= angle_deg < 300:
                direction = "6 o'clock"
            elif 300 <= angle_deg < 330:
                direction = "5 o'clock"
            elif 330 <= angle_deg < 360:
                direction = "4 o'clock"
            else:
                direction = "Unknown Clock Position"

            distance_rounded = format(distance, ".2f")
            print(distance_rounded)
            detections.append(videostream_pb2.DetectionResult(
                label=target_object,
                direction=direction,
                distance=distance_rounded))
        return detections

    def width_calculation(self, obj):
        real_width = 0.15
        target_object = obj.lower()

        if target_object in self.object_dimensions:
            real_width = float(self.object_dimensions[target_object])

        return target_object, real_width

    def decode_frame(self, video_frame):
        try:
            # Dimensions of Y plane are provided
            y_width, y_height = video_frame.y_width, video_frame.y_height

            # Calculate dimensions of U and V planes for YUV420
            uv_width, uv_height = y_width, y_height // 2

            # Handling Y plane
            Y = np.frombuffer(video_frame.y_plane, dtype=np.uint8).reshape((y_height, y_width))

            # Handling U plane
            u_data = np.frombuffer(video_frame.u_plane, dtype=np.uint8)
            u_data_padded = np.pad(u_data, (0, 1), 'constant', constant_values=0)
            U = u_data_padded.reshape((uv_height, uv_width))  # Adjust width for extra padding

            # Handling V plane
            v_data = np.frombuffer(video_frame.v_plane, dtype=np.uint8)
            v_data_padded = np.pad(v_data, (0, 1), 'constant', constant_values=0)
            V = v_data_padded.reshape((uv_height, uv_width))  # Adjust width for extra padding

            # Resize U and V to match Y dimensions
            U = cv.resize(U, (y_width, y_height), interpolation=cv.INTER_LINEAR)
            V = cv.resize(V, (y_width, y_height), interpolation=cv.INTER_LINEAR)

            # Merge Y, U, and V into a single YUV image
            YUV = cv.merge([Y, U, V])

            # Convert YUV to RGB
            rgb = cv.cvtColor(YUV, cv.COLOR_YUV2BGR)
            rgb = cv.rotate(rgb,
                            cv.ROTATE_90_CLOCKWISE)  # Use ROTATE_90_COUNTERCLOCKWISE to rotate
            # in the opposite direction

            return rgb
        except Exception as e:
            print(f"Error decoding frame: {e}")
            return None
