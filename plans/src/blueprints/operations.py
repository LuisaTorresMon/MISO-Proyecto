from flask import Flask, jsonify, make_response, request, Blueprint
from src.commands.create import Create
from src.commands.update import Update
from src.commands.getactivecontract import GetActiveContract


operations_blueprint = Blueprint('operations', __name__)

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
    return Update(data).execute()

# Consultar el plan activo
@operations_blueprint.route('/get/<int:empresa_id>', methods = ['GET'])
def get(empresa_id):
    result = GetActiveContract(empresa_id).execute()
    return result

# Consultar la salud del microservicio
@operations_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200

