import os

from app import create_app
from personservicer import start_grpc_server

app = create_app(os.getenv("FLASK_ENV") or "test")
start_grpc_server()

if __name__ == "__main__":
    app.run(debug=True)
