from flask import Blueprint, request, jsonify
from ..service.service import PaymentService
import logging

payment_blueprint = Blueprint('payment', __name__)
payment_service = PaymentService()

@payment_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

    


