from app.utils.shared_storage import storage
import app.proto.videostream_pb2 as videostream_pb2
import app.proto.videostream_pb2_grpc as videostream_pb2_grpc
from app.utils.word_approximation import load_model, find_closest_classes
class ConfigurationService(videostream_pb2_grpc.ConfigurationServiceServicer):
    def __init__ (self):
        self.model = load_model()


    def SetupDetection(self, request,context):
        user_question = request.user_question
        objects = self.configure_detection(user_question)
        storage.set_data('target_objects', objects)
        return videostream_pb2.SetupResponse(
            success=True,
            message="Configuration successful",
            objects_to_detect=list(map(str, objects))
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

        
        if user_question == "":
            objects = []
        else:
            objects = find_closest_classes(user_question, self.model, class_names)

        return objects

    