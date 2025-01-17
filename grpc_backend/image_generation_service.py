import grpc
from concurrent import futures
import service_definitions.generated.multi_service_pb2 as multi_service_pb2
import service_definitions.generated.multi_service_pb2_grpc as multi_service_pb2_grpc

# Implement Service A
class ImageServicer(multi_service_pb2_grpc.ImageServicer):
    def TextToImageGeneration(self, request, context):
        print(f"Service TextToImageGeneration received: {request.text}")

        # write to disk

        # Send the response back to the client
        return multi_service_pb2.MessageResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    multi_service_pb2_grpc.add_ImageServicer_to_server(ImageServicer(), server)
    server.add_insecure_port("[::]:50043")
    print("Service TextToImageGeneration is running on port 50043...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()