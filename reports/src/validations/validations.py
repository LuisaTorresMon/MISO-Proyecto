import logging

from ..errors.errors import CamposFaltantes, TokenVencido, ErrorService, TokenNoEnviado
from ..utils.utils import CommonUtils
from dotenv import load_dotenv
import os
import requests

load_dotenv('.env.template')
USER_URL = os.environ.get('USER_PATH')

common_utils = CommonUtils()

class ValidatorReports():
    def validar_campos_requeridos(self):
        if not self.nombre_reporte:
            raise CamposFaltantes("El campo nombre de reporte esta vacío, recuerda que es obligatorio")   
    
    def valid_token(self, token):
            headers = common_utils.obtener_token(token)
            url = f"{USER_URL}/auth/validate-token"

            response = requests.post(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                raise TokenVencido('')
            else:
                raise ErrorService('')   
            
    def validate_token_sent(self, token):
        if token is None:
            raise TokenNoEnviado('No se ha enviado el token')