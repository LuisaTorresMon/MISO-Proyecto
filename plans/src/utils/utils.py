import os
from flask import request
import requests
from src.errors.errors import TokenVencido, ErrorServicio
import logging

#USERS_PATH = os.getenv('USERS_PATH', 'http://localhost:3000')

class FileUtils():

    def get_user(self, headers):
        token_encabezado = headers.get('Authorization')
        token_sin_bearer = token_encabezado[len('Bearer '):]
        logging.debug(f"token sin bearer {token_sin_bearer}")

        headers = {
            'Authorization': f"Bearer {token_sin_bearer}",
        }

        response = requests.get(url='http://users:3000/users/me', headers=headers)

        logging.debug(f"codigo de respuesta {response.text}")
        if response.status_code == 200:
            data = response.json()
            return data['id']
        elif response.status_code == 401:
            raise TokenVencido
        else:
            raise ErrorServicio
        