from flask import jsonify, Flask
from flask_cors import CORS
from .config.config import Config
import logging
from .blueprints.blueprints import incident_blueprint
from .errors.errors import ApiError

app = Config.init()

cors = CORS(app)

logging.basicConfig(level=logging.DEBUG) 

app.register_blueprint(incident_blueprint, url_prefix='/incident')

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3004, debug=True)