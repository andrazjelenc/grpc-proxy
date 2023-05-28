from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import urlparse, parse_qs

import grpc
import app_pb2
import app_pb2_grpc

PAYLOAD_PREFIX = 'payload_'
METADATA_PREFIX = 'metadata_'

GRPC_SERVER = "localhost:50051"
GRPC_METHOD_MAPPINGS = {
    "LoginUser": "LoginUserRequest",
    "RegisterUser": "RegisterUserRequest",
    "GetInfo": "GetInfoRequest"
}


def send_qrpc(method, payload_parameters, metadata_parameters):
    print(f"Method {method} with payload {str(payload_parameters)} and metadata {str(metadata_parameters)}.")

    if method not in GRPC_METHOD_MAPPINGS:
        return "Forbidden method!"
    
    with grpc.insecure_channel(GRPC_SERVER) as channel:
        stub = app_pb2_grpc.SimpleAppStub(channel)

        grpc_method = getattr(stub, method, None)
        if not callable(grpc_method):
            return "Not callable method!"
        
        grpc_message = getattr(app_pb2, GRPC_METHOD_MAPPINGS[method], None)
        if not callable(grpc_message):
            return "Not callable message!"
        
        try:
            response = grpc_method(grpc_message(**payload_parameters), metadata=list(metadata_parameters.items()))
            print(response.message)
            return response.message
        except Exception as e:
            print(e)
            return "Exception!"

def extract_parameters(parameters, prefix):
    return {key[len(prefix):]: value[0] for key,value in parameters.items() if key.startswith(prefix)}

def middleware_server(host_port,content_type="text/plain"):
    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()

            parameters = parse_qs(urlparse(self.path).query)

            method = parameters.get('method')
            if method is None:
                content = 'Missing method parameter'
                self.wfile.write(content.encode())
                return

            payload_parameters = extract_parameters(parameters, PAYLOAD_PREFIX)
            metadata_parameters = extract_parameters(parameters, METADATA_PREFIX)

            content = send_qrpc(method[0], payload_parameters, metadata_parameters)
            self.wfile.write(content.encode())
            return

    class _TCPServer(TCPServer):
        allow_reuse_address = True

    httpd = _TCPServer(host_port, CustomHandler)
    httpd.serve_forever()


print("Starting Proxy Server")
print("Send payloads in http://localhost:8081/")

try:
    middleware_server(('0.0.0.0',8081))
except KeyboardInterrupt:
    pass
