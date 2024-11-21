# subscriber.py
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import logging
import json
import os
from ..config.config import Config
from ..service.service import Service

load_dotenv('.env.template')

project_id = os.environ.get('PROJECT_ID', '')
subscription_id = os.environ.get('SUBSCRIPTION_ID_IA_REQUEST', '')

app = None
ia_service = Service()

def callback(message):
    global app

    if app is None:
        logging.debug('creando contexto')
        app = Config.init()

    with app.app_context():
        logging.debug(f"Recibido mensaje 1: {message.data}")
        ia_data = message.data.decode('utf-8')
        incidence = json.loads(ia_data)["incidence"]
        logging.debug(f"Recibido mensaje 2: {incidence}")
        prediction = ia_service.predict_ia(incidence["asunto"], incidence["descripcion"])
        publish_ia_response(incidence, prediction)
        message.ack()


def subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Comienza a escuchar el topic
    future = subscriber.subscribe(subscription_path, callback=callback)
    logging.debug(f"Esperando mensajes en {subscription_path}...\n")

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()


def publish_ia_response(incidence, context):

    publisher = pubsub_v1.PublisherClient()

    topic_name = f"projects/{project_id}/topics/ia-prediction-topic"

    message_body = json.dumps({
        "incidence_id": incidence["id"],
        "prediction": context
    })

    attributes = {
        "type": "response"
    }

    future = publisher.publish(topic_name, message_body.encode("utf-8"), **attributes)
    logging.debug(f"Mensaje a topic de ia enviado con filtro response: {future.result()}")
