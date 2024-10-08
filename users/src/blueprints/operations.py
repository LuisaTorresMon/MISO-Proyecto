from flask import Flask, jsonify, make_response, request, Blueprint
from ..service.service import UserService

users_blueprint = Blueprint('users', __name__)
user_service = UserService()

# Crear usuario
@users_blueprint.route('/create', methods = ['POST'])
def create():
    data = request.get_json()
    result = user_service.create_user(data)
    return make_response(result, 201)

@users_blueprint.route('/register/client', methods = ['POST'])
def register():
    data = request.get_json()
    result = user_service.register_client(data)
    return result

@users_blueprint.route("/auth/signin", methods = ["POST"])
def signIn():
    data = request.get_json()
    result = user_service.signIn(data)
    return make_response(result, 200)

# Consultar la salud del microservicio
@users_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200