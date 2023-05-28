# grpc-proxy
Proxy REST to gRPC service.

## How to deploy

Setup virtual environment and install dependencies:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

Modify `app.proto` definitions to match definitions of your gRPC endpoint and recompile python stub. 
```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. app.proto
```

In `proxy.py` modify `GRPC_SERVER` to point to your gRPC endpoint and `GRPC_METHOD_MAPPINGS` to match mapping between gRPC methods and request messages. 

Start `proxy.py` app.
```
python proxy.py
```

## How to use
Open browser and navigate to `http://localhost:8081/?method=X&payload_key1=value1&payload_key2=value2&metadata_key3=value3` and the proxy will send request to method `X` with `key1=value1 key2=value2` payload and `key3=value3` metadata.
