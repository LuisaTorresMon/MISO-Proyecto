import os
import time
from os import environ

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError
from .models.model import db
from dotenv import load_dotenv
from flask_migrate import Migrate

app = Flask(__name__)
load_dotenv('.env.template')

db_url = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_url}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

cors = CORS(app)

app_context = app.app_context()
app_context.push()

db.init_app(app)

db.create_all()
migrate = Migrate(app, db)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code

app.register_blueprint(operations_blueprint,url_prefix='/report')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3005, debug=True)