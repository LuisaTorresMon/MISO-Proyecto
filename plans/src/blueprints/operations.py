from flask import Flask, jsonify, make_response, request, Blueprint
from src.commands.get import Get
from src.commands.list import List

operations_blueprint = Blueprint('operations', __name__)

# Consultar todos los planes
@operations_blueprint.route('/plans', methods = ['GET'])
def list():
    result = List().execute()
    return make_response(result, 200)

# Consultar un plan especifico
@operations_blueprint.route('/plans/<string:planId>', methods = ['GET'])
def get(planId):
    result = Get(planId).execute()
    return make_response(result, 200)

# Consultar la salud del microservicio
@operations_blueprint.route('/plans/ping', methods = ['GET'])
def health():
    return 'pong', 200
