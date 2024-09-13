from flask import Flask, jsonify, make_response, request, Blueprint
from src.commands.get import Get
from src.commands.list import List
from src.commands.create import Create

operations_blueprint = Blueprint('operations', __name__)

# Consultar todos los planes
@operations_blueprint.route('/list', methods = ['GET'])
def list():
    result = List().execute()
    return make_response(result, 200)

# Consultar un plan especifico
@operations_blueprint.route('/get/<string:planId>', methods = ['GET'])
def get(planId):
    result = Get(planId).execute()
    return make_response(result, 200)

# Crear contrato del plan escogido
@operations_blueprint.route('/contract', methods = ['POST'])
def create():
    data = request.get_json()
    result = Create(data).execute()
    return make_response(result, 201)

# Consultar la salud del microservicio
@operations_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200
