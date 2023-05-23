from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import unquote, urlparse, parse_qs

import grpc
import app_pb2
import app_pb2_grpc


grpc_server = "localhost:50051"

def send_qrpc(method, payload):
    print(method + " " + str(payload))
    
    with grpc.insecure_channel(grpc_server) as channel:
        stub = app_pb2_grpc.SimpleAppStub(channel)

        if method == 'LoginUser':
            response = stub.LoginUser(app_pb2.LoginUserRequest(username=payload['username'], password=payload['password']))

        elif method == 'RegisterUser':
            response = stub.RegisterUser(app_pb2.RegisterUserRequest(username=payload['username'], password=payload['password']))

        elif method == 'GetInfo':
            metadata = [('token', payload['token'])]
            response = stub.GetInfo(app_pb2.GetInfoRequest(id=payload['id']), metadata=metadata)
        
        return response.message


def middleware_server(host_port,content_type="text/plain"):

    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            try:
                parsed_url = urlparse(self.path)
                method = parse_qs(parsed_url.query)['method'][0]

                if method == 'LoginUser' or method == 'RegisterUser':
                    payload = {
                        'username': parse_qs(parsed_url.query)['username'][0],
                        'password': parse_qs(parsed_url.query)['password'][0]
                    }
                elif method == 'GetInfo':
                    payload = {
                        'id': parse_qs(parsed_url.query)['id'][0],
                        'token': parse_qs(parsed_url.query)['token'][0]
                    }
                else:
                    method = None
            except:
                method = None
                payload = None
                
            if method and payload:
                content = send_qrpc(method, payload)
            else:
                content = 'Wrong parameters!'

            self.send_header("Content-type", content_type)
            self.end_headers()
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
