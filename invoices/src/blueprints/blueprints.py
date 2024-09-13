from flask import Blueprint, request, jsonify
from ..service.service import InvoiceService
import logging

invoice_blueprint = Blueprint('invoices', __name__)
invoice_service = InvoiceService()

@invoice_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@invoice_blueprint.route('/create', methods=['POST'])
def create_invoice():
    
    invoice_data = request.get_json()
    logging.debug(invoice_data)

    invoice_saved = invoice_service.create_invoice(invoice_data)
    
    return jsonify({'invoice': invoice_saved}), 201    

@invoice_blueprint.route('/list', methods=['GET'])
def list_invoice():
    return invoice_service.get_invoices()
    
@invoice_blueprint.route('/pay', methods=['POST'])
def pay_invoice():
    
    data = request.get_json()
    logging.debug(data)

