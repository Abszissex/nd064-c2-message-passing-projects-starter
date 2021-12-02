
from kafka import KafkaConsumer
import os

from app.udaconnect.services import LocationService

KAFKA_SERVER = os.environ.get("KAFKA_SERVER")
TOPIC_NAME = 'new_location'

import json

def init_consumer():
    print("Init Kafka Consumer")
    print(f"Kafka Server: {KAFKA_SERVER}")
    print(f"Kafka Topic: {TOPIC_NAME}")
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
    for message in consumer:
        loc = json.loads(message.value)
        try:
            LocationService.create(loc)
        except Exception as e:
            print(f"Failed to create location: {e}")
            




