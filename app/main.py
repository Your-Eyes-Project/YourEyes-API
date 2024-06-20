import asyncio
import grpc
from ultralytics import YOLO
import app.proto.videostream_pb2_grpc as videostream_pb2_grpc
from app.services.video_streamer import VideoStreamerServicer
from app.services.configuration import ConfigurationService
from app.utils.shared_storage import storage
import logging
logging.basicConfig(level=logging.DEBUG)

async def serve():
    # Create a gRPC server
    server = grpc.aio.server()
    
    # Initialize the shared storage (if needed)
    storage.set_data('target_objects', [])

    # Load the YOLO model
    model = YOLO("yolov9c.pt")
    
    # Create service instances
    video_streamer_service = VideoStreamerServicer(model)
    configuration_service = ConfigurationService()
    
    # Add services to the gRPC server
    videostream_pb2_grpc.add_VideoStreamerServicer_to_server(video_streamer_service, server)
    videostream_pb2_grpc.add_ConfigurationServiceServicer_to_server(configuration_service, server)

    # Bind the server to the specified port
    server.add_insecure_port('[::]:5270')
    
    logging.info("Server is starting on port 5270...")
    
    # Start the server
    await server.start()
    
    try:
        # Keep the server running until manually interrupted
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Gracefully shut down the server on interruption
        await server.stop(None)

if __name__ == '__main__':
    # Run the serve coroutine
    asyncio.run(serve())
