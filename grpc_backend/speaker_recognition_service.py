import grpc
from concurrent import futures
import service_definitions.generated.multi_service_pb2 as multi_service_pb2
import service_definitions.generated.multi_service_pb2_grpc as multi_service_pb2_grpc

# Implement Service A
class SpeakerServicer(multi_service_pb2_grpc.SpeakerServicer):
    def TextToImageGeneration(self, request, context):
        print(f"Service SpeakerRecognition received: {request.text}")

        # write to disk

        # Send the response back to the client
        return multi_service_pb2.MessageResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    multi_service_pb2_grpc.add_SpeakerServicer_to_server(SpeakerServicer(), server)
    server.add_insecure_port("[::]:50044")
    print("Service SpeakerRecognition is running on port 50044...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()