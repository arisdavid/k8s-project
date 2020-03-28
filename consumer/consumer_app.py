import argparse
import os

from pykafka import KafkaClient
import logging

logging.basicConfig(level=logging.INFO)

client = KafkaClient(hosts=os.getenv('KAFKA_HOST'))


def get_message(topic):
    topic = client.topics[topic]
    consumer = topic.get_simple_consumer()
    for message in consumer:
        if message is not None:
            print((message.offset, message.value))


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Get messages from a kafka topic")
    parser.add_argument('topic', help='kafka topic')
    args = parser.parse_args()

    _topic = str(args.topic)

    if _topic is None:
        raise Exception('Please make sure to provide topic')

    get_message(_topic)
