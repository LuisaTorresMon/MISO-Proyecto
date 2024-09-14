# subscriber.py
from google.cloud import pubsub_v1
from dotenv import load_dotenv
from ..service.service import PaymentService
import logging
import json
import os
from ..config.config import Config

load_dotenv('.env.template')       

project_id = os.environ.get('PROJECT_ID', '')
subscription_id = os.environ.get('SUBSCRIPTION_ID', '')

payment_service = PaymentService()

def callback(message):
    logging.debug('creando contexto') 
    Config.init() 
       
    logging.debug(f"Recibido mensaje: {message.data}")
    message.ack()  
    
    payment_data = message.data.decode('utf-8')

    payment_service.procesar_cola(json.loads(payment_data))

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

