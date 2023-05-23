# grpc-proxy
Proxy between REST and gRPC service.

## Deploy

First setup virtual environment and install dependencies:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

Start `server.py` that accepts gRPC traffic:
```
python server.py
```

Start `proxy.py` that accepts REST traffic and forwards it to server via gRPC:
```
python proxy.py
```

## Recompile proto schema

Modify `app.proto` and run following command. It will recreate `app_pb2.py` and `app_bp2_grpc.py`. Check if python code needs some fixes too.
```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. app.proto
```