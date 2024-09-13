from flask import jsonify, Flask
from flask_cors import CORS
from .config.config import Config
from .blueprints.blueprints import invoice_blueprint
import logging

app = Config.init()

cors = CORS(app)

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(invoice_blueprint, url_prefix='/invoice')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True)