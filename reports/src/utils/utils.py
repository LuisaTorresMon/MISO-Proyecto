from dotenv import load_dotenv
from os import environ
import logging

class CommonUtils():
    def obtener_token(self, token):
        
        token_sin_bearer = token[len('Bearer '):]
        logging.debug(f"token sin bearer {token_sin_bearer}")
        
        headers = {
           "Authorization": f"Bearer {token_sin_bearer}",
        }
        return headers
        