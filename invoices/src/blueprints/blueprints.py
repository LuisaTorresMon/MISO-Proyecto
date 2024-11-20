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

@invoice_blueprint.route('/create/<int:month>/<int:empresa_id>/<string:lang>', methods=['POST'])
def get_invoice_by_enterprise(month, empresa_id,lang):
    
    headers = request.headers
    token_encabezado = headers.get('Authorization')
    logging.debug(token_encabezado)
         
    validator_invoice.validate_token_sent(token_encabezado)
    validator_invoice.valid_token(token_encabezado)
    
    invoice_response = invoice_service.build_invoice_client(token_encabezado, month, empresa_id, lang)

    return invoice_response, 201

@invoice_blueprint.route('/update/<int:invoice_id>/<string:state>', methods=['PATCH'])
def update_invoice_state(invoice_id, state):

    invoice_updated = invoice_service.update_state_invoice(state, invoice_id)    
    return jsonify({'invoice': invoice_updated}), 201   

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

@invoice_blueprint.route('/pay', methods = ['POST'])
def pay_invoice():
    headers = request.headers
    token_encabezado = headers.get('Authorization')
    logging.debug(token_encabezado)
         
    validator_invoice.validate_token_sent(token_encabezado)
    validator_invoice.valid_token(token_encabezado)
    
    request_data = request.get_json()
    
    id_invoice = request_data.get('id_invoice')
    payment_method_id = request_data.get('payment_method_id')
    
    validator_invoice.validate_data_pay(id_invoice, payment_method_id)
    
    invoice_service.pay_menthod_queue(id_invoice, payment_method_id) 
    
    return {"msg": 'Registro encolado con exito'}, 201


