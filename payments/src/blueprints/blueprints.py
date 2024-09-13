from flask import Blueprint, request, jsonify
from ..service.service import PaymentService
import logging

payment_blueprint = Blueprint('payment', __name__)
payment_service = PaymentService()

@payment_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@payment_blueprint.route('/create', methods=['POST'])
def create_payment():
    
    payment_data = request.get_json()
    logging.debug(payment_data)

    payment_saved = payment_service.create_payment(payment_data)
    
    return jsonify({'payment': payment_saved}), 201    

@payment_blueprint.route('/list', methods=['GET'])
def list_payment():
    return payment_service.get_payments()
    


