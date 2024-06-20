from app.utils.shared_storage import storage
import app.proto.videostream_pb2 as videostream_pb2
import app.proto.videostream_pb2_grpc as videostream_pb2_grpc

class ConfigurationService(videostream_pb2_grpc.ConfigurationServiceServicer):

    def SetupDetection(self, request, context):
        user_question = request.user_question.lower()
        print("Received question:", user_question)

        objects = self.configure_detection(user_question)
        storage.set_data('target_objects', objects)
        return videostream_pb2.SetupResponse(
            success=True,
            message="Configuration successful",
            objects_to_detect=objects
        )

    def configure_detection(self, user_question):
        class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train",
                       "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", 
                       "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", 
                       "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", 
                       "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", 
                       "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", 
                       "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", 
                       "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", 
                       "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", 
                       "tvmonitor", "laptop", "mouse", "remote", "keyboard", "telephone", 
                       "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", 
                       "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

        words = user_question.split()
        print(words)
        objects = [class_names.index(word) for word in words if word in class_names]

        return objects
