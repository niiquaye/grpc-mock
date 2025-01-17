import grpc
from concurrent import futures
import service_definitions.generated.multi_service_pb2 as multi_service_pb2
import service_definitions.generated.multi_service_pb2_grpc as multi_service_pb2_grpc

# Implement Service A
class SummarizerServicer(multi_service_pb2_grpc.SummarizerServicer):
    def SummarizeText(self, request, context):
        print(f"Service Summarizer received: {request.text}")

        # summarize text then forward to other ML models 
        
        # Forward the request to Audio Generation
        with grpc.insecure_channel("localhost:50042") as channel:
            stub = multi_service_pb2_grpc.ServiceBStub(channel)
            response = stub.AudioStub(multi_service_pb2.StringRequest(text=request.text))
            if response.success:
                print("Audio Generation complete")

        # Forward the request to Image Generation
        with grpc.insecure_channel("localhost:50043") as channel:
            stub = multi_service_pb2_grpc.ServiceBStub(channel)
            response = stub.ImageStub(multi_service_pb2.StringRequest(text=request.text))
            if response.success:
                print("Image Generation Complete")

        # Forward the request to Speaker Recognmition
        with grpc.insecure_channel("localhost:50044") as channel:
            stub = multi_service_pb2_grpc.ServiceBStub(channel)
            response = stub.SpeakerStub(multi_service_pb2.StringRequest(text=request.text))
            if response.success:
                print("Speaker Recognition Complete")

        # Send the response back to the client
        return multi_service_pb2.StringResponse(text=f"Summarizer Complete")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    multi_service_pb2_grpc.add_SummarizerServicer_to_server(SummarizerServicer(), server)
    server.add_insecure_port("[::]:50041")
    print("Service Summarizer is running on port 50041...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()