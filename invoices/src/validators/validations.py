import logging
from dotenv import load_dotenv
from ..error.errors import InvoiceGeneralIntegration
from ..utils.utils import CommonUtils
import os
import requests

load_dotenv('.env.template')
USER_URL = os.environ.get('USER_PATH')

common_utils = CommonUtils()
class ValidatorInvoice():
    
    def valid_token(self, token):
            headers = common_utils.obtener_token(token)
            url = f"{USER_URL}/auth/validate-token"

            response = requests.post(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                raise InvoiceGeneralIntegration(401, 'El token no es válido o está vencido.')
            else:
                raise InvoiceGeneralIntegration(403, 'Error a la hora de consumir el servicio')   
            
    def validate_token_sent(self, token):
        if token is None:
            raise InvoiceGeneralIntegration(403, 'No se ha enviado el token')