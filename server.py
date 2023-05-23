from concurrent import futures

import grpc
import app_pb2
import app_pb2_grpc

SECRET_TOKEN = 'abcdef12345'


class SimpleApp(app_pb2_grpc.SimpleAppServicer):
    def LoginUser(self, request, context):
        username = request.username
        password = request.password
        print(f"LoginUser: ({username}, {password})")

        context.send_initial_metadata((
            ('token', ''),
        ))
        context.set_trailing_metadata((
            ('token', SECRET_TOKEN),
        ))

        return app_pb2.LoginUserResponse(message='Your id is 123.')
	
    def RegisterUser(self, request, context):
        username = request.username
        password = request.password
        print(f"RegisterUser: ({username}, {password})")

        return app_pb2.RegisterUserResponse(message=f'Account for {username} created!')

    def GetInfo(self, request, context):
        id = request.id
        token = dict(context.invocation_metadata()).get('token')
        print(f"GetInfo ({id}, token: {token})")
        if token is None:
            return app_pb2.GetInfoResponse(message=f'Token missing :(')
        elif token != SECRET_TOKEN:
            return app_pb2.GetInfoResponse(message=f'Invalid token :(')
        
        return app_pb2.GetInfoResponse(message=f'Welcome dear user with id {id}.')


def server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
   app_pb2_grpc.add_SimpleAppServicer_to_server(SimpleApp(), server)
   server.add_insecure_port('[::]:50051')
   print("gRPC starting")
   server.start()
   server.wait_for_termination()


if __name__ == "__main__":
    server()
