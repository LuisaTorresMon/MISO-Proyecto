from flask import Flask, jsonify, make_response, request, Blueprint
from ..service.service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

users_blueprint = Blueprint('users', __name__)
user_service = UserService()

# Crear usuario
@users_blueprint.route('/create', methods = ['POST'])
def create():
    data = request.get_json()
    result = user_service.create_user(data)
    return make_response(result, 201)

@users_blueprint.route('/register/client', methods = ['POST'])
def register_client():
    data = request.get_json()
    result = user_service.register_client(data)
    return result

@users_blueprint.route('/register/user', methods = ['POST'])
def register_user():
    data = request.get_json()
    result = user_service.register_user(data)
    return result

@users_blueprint.route('/register/agent', methods = ['POST'])
def register_agent():
    data = request.get_json()
    result = user_service.register_agent(data)
    return result

@users_blueprint.route("/auth/login", methods = ["POST"])
def signIn():
    data = request.get_json()
    result = user_service.signIn(data)
    return make_response(result, 200)

@users_blueprint.route("/auth/validate-token", methods=["POST"])
@jwt_required()
def validate_token():
    current_jwt = get_jwt()
    return make_response(current_jwt), 200


# Consultar la salud del microservicio
@users_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200
