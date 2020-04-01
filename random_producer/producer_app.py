import argparse
import logging
import os
import time
from datetime import datetime

import faker
from pykafka import KafkaClient

logging.basicConfig(level=logging.INFO)

client = KafkaClient(hosts=os.getenv("KAFKA_HOST"))


def publish_random_records(topic):

    topic = client.topics[topic]
    with topic.get_sync_producer() as producer:
        while True:
            f = faker.Faker()
            contact = dict(
                username=f.user_name(),
                email=f.email(),
                first_name=f.first_name(),
                last_name=f.last_name(),
                date_created=datetime.utcnow(),
            )
            logging.info(f"Publishing message {contact} to {topic}.")
            producer.produce(str(contact).encode())
            logging.info(f"Message published.")

            time.sleep(5)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Generated random contacts")
    parser.add_argument("topic", help="Kafka topic")
    args = parser.parse_args()

    _topic = str(args.topic)

    if _topic is None:
        raise Exception("Please make sure to provide a topic")

    publish_random_records(_topic)
