from flask import Blueprint, request, make_response
from ..service.service import Service
ia_blueprint = Blueprint('ia', __name__)

service = Service()

@ia_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@ia_blueprint.route('/sync', methods=['POST'])
def online():
    data = request.get_json()
    prediction = service.predict_ia("", data["context"])
    return make_response(
        {"prediction": prediction},
        200
    )