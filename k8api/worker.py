import argparse
import uuid

from kubernetes import client, config

config.load_kube_config()


def create_producer_container(topic):

    label = "contacts-producer"
    image_pull_policy = "Never"
    container = client.V1Container(name=label, image_pull_policy=image_pull_policy)
    container.image = "contacts-producer-app:latest"
    container.args = [topic]
    container.env = [
        {"name": "KAFKA_HOST", "value": "k8-kafka.k8demo.svc.cluster.local:9092"}
    ]

    return container


def create_job(topic):

    metadata = client.V1ObjectMeta(
        name=f"kafka-publisher-{uuid.uuid4()}", labels={"name": "contacts-producer"},
    )

    pod_template = client.V1PodTemplateSpec(metadata=metadata)
    pod_template.spec = client.V1PodSpec(
        containers=[create_producer_container(topic)], restart_policy="Never"
    )

    job = client.V1Job(
        spec=client.V1JobSpec(backoff_limit=0, template=pod_template),
        metadata=metadata,
        kind="Job",
        api_version="batch/v1",
    )

    return job


def launch_kakfa_producer(topic):

    namespace = "k8demo"
    batch_api = client.BatchV1Api()
    batch_api.create_namespaced_job(namespace, create_job(topic))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Launch a producer pod programmatically."
    )
    parser.add_argument("topic", help="Kafka topic to publish to")

    args = parser.parse_args()

    launch_kakfa_producer(args.topic)
