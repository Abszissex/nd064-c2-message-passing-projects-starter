import logging
from typing import Dict

from app.udaconnect.schemas import LocationSchema
import os
from kafka import KafkaProducer
import json
from datetime import datetime


KAFKA_SERVER = os.environ.get("KAFKA_SERVER")


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


TOPIC_NAME = 'new_location'


import time

def current_milli_time():
    return round(time.time() * 1000)


def publish_to_kafka(message: Dict):
    print(f"Publishing to Kafka: {KAFKA_SERVER} - {TOPIC_NAME}")
    """
    Publish a message to a Kafka topic.
    """
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(TOPIC_NAME, message)
        producer.flush()
    except Exception as e:
        logger.error(f"Failed to publish to Kafka: {e}")
        raise e




class LocationService:
    @staticmethod
    def create(location: Dict):


        location['creation_time'] = str(datetime.utcnow())
        loc = LocationSchema().load(location)
        publish_to_kafka(location)