from flask import Flask, jsonify, make_response, request, Blueprint
from src.commands.get import Get
from src.commands.list import List
from src.commands.create import Create
from src.commands.update import Update
from src.commands.getactivecontract import GetActiveContract


operations_blueprint = Blueprint('operations', __name__)

# Consultar todos los planes
@operations_blueprint.route('/list', methods = ['GET'])
def list():
    result = List().execute()
    return make_response(result, 200)

# Consultar el plan activo
@operations_blueprint.route('/get/<int:empresa_id>', methods = ['GET'])
def get(empresa_id):
    result = GetActiveContract(empresa_id).execute()
    return result

# Crear contrato del plan escogido
@operations_blueprint.route('/contract', methods = ['POST'])
def create():
    data = request.get_json()
    result = Create(data).execute()
    return make_response(result, 201)

# Actualizar contrato con otro plan
@operations_blueprint.route('/update/contract', methods = ['POST'])
def update():
    data = request.get_json()
    contract_data, status_code = Update(data).execute()
    return make_response(jsonify(contract_data), status_code)


# Consultar la salud del microservicio
@operations_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200
