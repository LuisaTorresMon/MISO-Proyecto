from flask import jsonify
from flask_cors import CORS
from .config.config import Config
import logging
from .blueprints.blueprints import ia_blueprint
from .errors.errors import ApiError
from .subscribe.subscribe_ia_request import subscribe
import threading

app = Config.init()

cors = CORS(app, resources={r"/*": {"origins": "*"}}, expose_headers=["Authorization", "Technology"])

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(ia_blueprint, url_prefix='/ia')

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code

def start_subscription():
    subscribe()

threading.Thread(target=start_subscription).start()
logging.debug('La descripcion ha comenzado')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3005, debug=True)