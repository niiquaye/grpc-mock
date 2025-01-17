import grpc

import service_definitions.generated.multi_service_pb2 as multi_service_pb2
import service_definitions.generated.multi_service_pb2_grpc as multi_service_pb2_grpc


def run():
    # grab text data from form data from fast API POST request
    with grpc.insecure_channel("localhost:50041") as channel:
        stub = multi_service_pb2_grpc.SummarizerStub(channel)
        text_to_send = "Hello from Client"
        response = stub.SummarizeText(multi_service_pb2.StringRequest(text=text_to_send))
        print(f"Client received: {response.text}")

if __name__ == "__main__":
    run()