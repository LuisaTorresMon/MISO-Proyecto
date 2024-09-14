from flask import jsonify, Flask
from flask_cors import CORS
from .config.config import Config
from .blueprints.blueprints import payment_blueprint
from .subcribe.subscribe import subscribe
import logging
import threading

app = Config.init()

cors = CORS(app)

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(payment_blueprint, url_prefix='/payment')

def start_subscription():
    with app.app_context():
        subscribe()

threading.Thread(target=start_subscription).start()
logging.debug('La descripcion ha comenzado')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)