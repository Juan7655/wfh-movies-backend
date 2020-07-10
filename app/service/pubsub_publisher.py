from google.cloud import pubsub_v1
from config import settings, log
from json import dumps

publisher = pubsub_v1.PublisherClient()


def publish(raw_data: dict):
    topic_path = publisher.topic_path(settings.project_id, settings.topic_name)

    raw_data = dumps(raw_data).encode("utf-8")
    publisher.publish(topic_path, data=raw_data)
    log.debug(f'message published: {raw_data}')
