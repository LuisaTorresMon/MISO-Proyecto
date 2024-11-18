from datetime import datetime
import logging
from flask import Flask, jsonify, make_response, request, Blueprint, send_file

from ..errors.errors import ServerSystemException, BadRequestException
from ..service.report_service import ReportService
from ..validations.validations import ValidatorReports

validator_report = ValidatorReports()
service_report = ReportService()

operations_blueprint = Blueprint('operations', __name__)

@operations_blueprint.route('/generate', methods = ['POST'])
def save_report():
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(f"Token recibido: {token_encabezado}")

        validator_report.validate_token_sent(token_encabezado)
        validator_report.valid_token(token_encabezado)

        data = request.get_json()
        if not data:
            raise BadRequestException("No se han enviado datos para el reporte")

        canal_id = data.get('canal_id')  
        estado_id = data.get('estado_id')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        nombre_reporte = data.get('nombre_reporte') 
        tipo_id = data.get('tipo_id')  

        validator_report.nombre_reporte = nombre_reporte
        validator_report.validar_campos_requeridos()

        fecha_inicio = datetime.strptime(fecha_inicio, '%m/%d/%Y') if fecha_inicio else None
        fecha_fin = datetime.strptime(fecha_fin, '%m/%d/%Y') if fecha_fin else None

        incidentes = service_report.fetch_incidents(
            canal_id=canal_id,
            estado_id=estado_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_id=tipo_id,
            token_encabezado=token_encabezado
        )

        service_report.save_report(
            nombre_reporte=nombre_reporte,
            estado_id=estado_id,
            tipo_id=tipo_id,
            canal_id=canal_id,
            incidentes=incidentes,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        pdf_file = service_report.generate_pdf_report(nombre_reporte, incidentes)

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name=f"{nombre_reporte}.pdf",
            mimetype='application/pdf'
        )

    except Exception as err:
        logging.debug(f"Excepción al guardar el reporte: {err}")
        raise ServerSystemException(f"Error al guardar el reporte: {err}, contacte con el administrador")
    
@operations_blueprint.route('/ping', methods = ['GET'])
def health():
    return 'pong', 200
