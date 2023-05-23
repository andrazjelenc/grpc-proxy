import grpc

import app_pb2
import app_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = app_pb2_grpc.SimpleAppStub(channel)

        print("Registration...")
        response = stub.RegisterUser(app_pb2.RegisterUserRequest(username='admin', password='admin123'))
        print(response.message)

        print("Login...")
        response, call = stub.LoginUser.with_call(app_pb2.LoginUserRequest(username='admin', password='admin123')) 
        print(response.message)
        token = dict(call.trailing_metadata()).get('token')
        print(f"Trailing token in metadata: {token}")
        
        print("Info...")
        metadata = [('token', token)]
        response = stub.GetInfo(app_pb2.GetInfoRequest(id='666'), metadata=metadata)
        print(response.message)

if __name__ == '__main__':
    run()
