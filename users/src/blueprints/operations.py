from flask import Flask, jsonify, make_response, request, Blueprint
from ..service.service import UserService
from ..errors.errors import ServerSystemException
from ..validators.validator import UserValidator
from flask_jwt_extended import jwt_required
import logging

users_blueprint = Blueprint('users', __name__)
user_service = UserService()
user_validator = UserValidator()

# Crear usuario
@users_blueprint.route('/create', methods = ['POST'])
def create():
    data = request.get_json()
    result = user_service.create_user(data)
    return make_response(result, 201)

# Crear usuario
@users_blueprint.route('/person', methods = ['GET'])
def find_person_by_identity():
    
    identity_type = request.args.get('identityType')
    identity_number = request.args.get('identityNumber')
    
    user_validator.validate_query_person(identity_type, identity_number)
    result = user_service.get_person_by_identity(identity_type, identity_number)
    return make_response(result, 201)

@users_blueprint.route("/auth/login", methods = ["POST"])
def signIn():
    data = request.get_json()
    result = user_service.signIn(data)
    return make_response(result, 200)

@users_blueprint.route("/auth/validate-token", methods=["POST"])
@jwt_required()
def validate_token():
    return make_response({"msg": "OK"}), 200


# Consultar la salud del microservicio
@users_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200