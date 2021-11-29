import os
from app import create_app
from app.udaconnect.kafka_consumer import init_consumer

app = create_app(os.getenv("FLASK_ENV") or "test")
app.app_context().push()

init_consumer()

if __name__ == "__main__":
    app.run(debug=True, port=6000)





