
from google.cloud import pubsub_v1
import logging
import os
import json

project_id = os.environ.get('PROJECT_ID', '')

def publish_ia_request(incidence, context):

    publisher = pubsub_v1.PublisherClient()

    topic_name = f"projects/{project_id}/topics/ia-prediction-topic"

    message_body = json.dumps({
        "incidence": incidence,
        "context": context
    })

    attributes = {
        "type": "request"
    }

    future = publisher.publish(topic_name, message_body.encode("utf-8"), **attributes)
    logging.debug(f"Mensaje a topic de ia enviado: {future.result()}")