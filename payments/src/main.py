from flask import jsonify, Flask
from flask_cors import CORS
from .config.config import Config
from .blueprints.blueprints import payment_blueprint
from .subcribe.subscribe import subscribe
from dotenv import load_dotenv
from os import environ
import logging
import threading

app = Config.init()

cors = CORS(app)

load_dotenv('.env.template')       

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(payment_blueprint, url_prefix='/payment')

is_testing = bool(environ.get('TESTING'))

def start_subscription():
    subscribe()

if is_testing == True:
    threading.Thread(target=start_subscription).start()
    logging.debug('La descripcion ha comenzado')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)