
from os import environ
from flask import Flask, jsonify

from .blueprints.operations import users_blueprint
from .errors.errors import ApiError
from .models.model import cargar_datos_iniciales, db
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta

app = Flask(__name__)
load_dotenv('.env.template')

db_url = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_url}"


'''
db_user = environ.get('DB_USER')
db_password = environ.get('DB_PASSWORD')
db_port = environ.get('DB_PORT')
db_name = environ.get('DB_NAME')
db_host = environ.get('DB_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
'''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

app_context = app.app_context()
app_context.push()

db.init_app(app)

db.create_all()
migrate = Migrate(app, db)
cargar_datos_iniciales()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code

jwt = JWTManager(app)

app.register_blueprint(users_blueprint,url_prefix='/user')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)