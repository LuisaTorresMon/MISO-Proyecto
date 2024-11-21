import json
import os

from dotenv import load_dotenv
#from google.cloud import storage

import os
import requests
from ..errors.errors import IAPredictionException
import logging

class CommonUtils:

    def get_ia_prediction(self, subject, context):
        logging.debug(context)
        if subject == "":
            role_user = {"role": "user", "content": f"El contexto es: {context}"}
        else:
            role_user = {"role": "user", "content": f"El asunto es: {subject}. El contexto es: {context}"}

        key = os.getenv("OPENAI_API_KEY")
        token = f'Bearer {key}'
        url = "https://api.openai.com/v1/chat/completions"
        logging.debug(token)
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
            {"role": "system", "content":
                f"Eres un agente de call center llamado ABCIA, siempre debes identificarte e intentar dar respuestas acordes a soluciones."},
            role_user
        ],
            "temperature": 0.7,
            "max_tokens": 100
        }

        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10000)

        if response.status_code == 200:
            response_data = response.json()
            assistant_message = response_data['choices'][0]['message']['content']
            logging.debug(f"Assistant: {assistant_message}")
            return assistant_message
        else:
            logging.debug("Error:", response.status_code, response.text)
            raise IAPredictionException(f"Error en la llamada a la API: {response.status_code} - {response.text}")

    def obtener_token(self, token):
        
        token_sin_bearer = token[len('Bearer '):]
        logging.debug(f"token sin bearer {token_sin_bearer}")
        
        headers = {
           "Authorization": f"Bearer {token_sin_bearer}",
        }
        return headers