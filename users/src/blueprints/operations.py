from flask import Flask, jsonify, make_response, request, Blueprint
from ..service.service import UserService
from ..validators.validator import UserValidator
from ..models.model import PersonSchema, EmpresaSchema
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

users_blueprint = Blueprint('users', __name__)
user_service = UserService()
user_validator = UserValidator()
person_schema = PersonSchema()
company_schema = EmpresaSchema()

# Crear usuario
@users_blueprint.route('/create', methods = ['POST'])
def create():
    data = request.get_json()
    result = user_service.create_user(data)
    return make_response(result, 201)

# Crear usuario
@users_blueprint.route('/person', methods = ['GET'])
@jwt_required()
def find_person_by_identity():
    
    identity_type = request.args.get('identityType')
    identity_number = request.args.get('identityNumber')
    
    user_validator.validate_query_person(identity_type, identity_number)
    person = user_service.get_person_by_identity(identity_type, identity_number)
    return make_response(person_schema.dump(person), 200)

@users_blueprint.route('/get/<int:id>', methods = ['GET'])
@jwt_required()
def find_user_by_id(id):
    user = user_service.get_user_by_id(id)
    return make_response(user, 200)

@users_blueprint.route('/get/username/<string:username>', methods = ['GET'])
@jwt_required()
def find_user_by_username(username):
    user = user_service.get_user_by_username(username)
    return make_response(user, 200)

@users_blueprint.route('/company/<int:id>', methods = ['GET'])
@jwt_required()
def find_company_by_id(id):
    company = user_service.get_company_by_id(id)
    return make_response(company_schema.dump(company), 200)

@users_blueprint.route('/person/<int:id>', methods = ['GET'])
@jwt_required()
def find_person_by_id(id):
    person = user_service.get_person_by_id(id)
    return make_response(person_schema.dump(person), 200)

@users_blueprint.route('/person/<int:id>/products', methods = ['GET'])
@jwt_required()
def get_products_by_person(id):
    products = user_service.get_products_by_person(id)
    return make_response(products, 200)


@users_blueprint.route('/person/create', methods = ['POST'])
@jwt_required()
def create_person():
    data = request.get_json()
    result = user_service.create_person(data)
    return make_response(result, 201)

@users_blueprint.route('/person/update', methods = ['PUT'])
@jwt_required()
def update_person():
    data = request.get_json()
    result = user_service.update_person(data)
    return make_response(result, 200)

@users_blueprint.route('/register/client', methods = ['POST'])
def register_client():
    data = request.get_json()
    result = user_service.register_client(data)
    return result

@users_blueprint.route('/register/agent', methods = ['POST'])
@jwt_required()
def register_agent():
    data = request.get_json()
    result = user_service.register_agent(data)
    return result

@users_blueprint.route('/register/user', methods = ['POST'])
def register_user():
    data = request.get_json()
    result = user_service.register_user(data)
    return make_response(result, 201)

@users_blueprint.route('/agent/<int:id_empresa>', methods = ['GET'])
@jwt_required()
def get_agents_by_company(id_empresa):
    result = user_service.get_agents_by_company(id_empresa)
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

@users_blueprint.route('/ia/user', methods = ['GET'])
def get_ia_user():
    headers = request.headers
    logging.debug(headers)
    ia_user = headers.get('x-ia-user')
    if not ia_user:
        result = user_service.get_user_by_username("agente_ia")
        return make_response(result, 200)