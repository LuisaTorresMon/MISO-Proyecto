from flask import Blueprint, request, jsonify, make_response
from ..service.service import InvoiceService
from ..validators.validations import ValidatorInvoice
import logging

invoice_blueprint = Blueprint('invoices', __name__)
invoice_service = InvoiceService()
validator_invoice = ValidatorInvoice()

@invoice_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@invoice_blueprint.route('/create/<int:month>/<int:empresa_id>', methods=['POST'])
def get_invoice_by_enterprise(month, empresa_id):
    
    headers = request.headers
    token_encabezado = headers.get('Authorization')
    logging.debug(token_encabezado)
         
    validator_invoice.validate_token_sent(token_encabezado)
    validator_invoice.valid_token(token_encabezado)
    
    invoice_response = invoice_service.build_invoice_client(token_encabezado, month, empresa_id)

    return invoice_response, 201

@invoice_blueprint.route('/create', methods=['POST'])
def create_invoice():
    
    invoice_data = request.get_json()
    logging.debug(invoice_data)

    invoice_saved = invoice_service.create_invoice(invoice_data)
    
    return jsonify({'invoice': invoice_saved}), 201    

@invoice_blueprint.route('/list', methods=['GET'])
def list_invoice():
    return invoice_service.get_invoices()

@invoice_blueprint.route('/send-email', methods=['POST'])
def send_invoice_by_email():
    
    headers = request.headers
    token_encabezado = headers.get('Authorization')
    logging.debug(token_encabezado)
         
    validator_invoice.validate_token_sent(token_encabezado)
    validator_invoice.valid_token(token_encabezado)
    
    request_data = request.get_json()
    logging.debug(request_data)
    
    email = request_data.get('email')
    invoice_id = request_data.get('invoice_id')
    lang = request_data.get('lang')

    response = invoice_service.send_invoice_pdf_by_email(token_encabezado, email, invoice_id, lang)
    
    return response, 201   

@invoice_blueprint.route('/get-invoice-pdf/<int:invoice_id>/<string:lang>', methods=['GET'])
def get_invoice_pdf(invoice_id, lang):
    
    headers = request.headers
    token_encabezado = headers.get('Authorization')
    logging.debug(token_encabezado)
         
    validator_invoice.validate_token_sent(token_encabezado)
    validator_invoice.valid_token(token_encabezado)
    
    pdf_json = invoice_service.get_invoice_pdf(token_encabezado, invoice_id, lang)
    response = make_response(pdf_json['pdf'])
    
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f"attachment; filename={pdf_json['file_name']}.pdf"
    return response
    
@invoice_blueprint.route('/pay', methods=['POST'])
def pay_invoice():
    
    data = request.get_json()
    logging.debug(data)

