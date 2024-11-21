# subscriber.py
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import logging
import os
import json
from ..service.incident_service import IncidentService
from ..config.config import Config

app = None

load_dotenv('.env.template')

incident_service = IncidentService()

project_id = os.environ.get('PROJECT_ID', '')
subscription_id = os.environ.get('SUBSCRIPTION_ID_IA_RESPONSE', '')

def callback(message):
    global app

    if app is None:
        logging.debug('creando contexto')
        app = Config.init()

    with app.app_context():
        logging.debug(f"Recibido mensaje 1: {message.data}")
        ia_data = message.data.decode('utf-8')
        data = json.loads(ia_data)
        logging.debug(f"Recibido mensaje 2: {data}")
        incident_service.update_incident_from_ia(data["prediction"], data["incidence_id"])
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

