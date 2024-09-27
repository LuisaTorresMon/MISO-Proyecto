from flask import Blueprint, request, jsonify
from ..validations.validations import ValidatorIncidents
import logging

incident_blueprint = Blueprint('incident', __name__)
validator_incident = ValidatorIncidents()

@incident_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return 'pong', 200

@incident_blueprint.route('/create', methods=['POST'])
def create_incidence():

    # Datos cliente
    nombre_cliente = request.form.get('nombre_cliente')     
    apellido_cliente = request.form.get('apellido_cliente')     
    correo_electronico_cliente = request.form.get('correo_electronico_cliente') 
    tipo_documento_cliente = request.form.get('tipo_documento_cliente')     
    numero_documento_cliente = request.form.get('numero_documento_cliente')  
    celular_cliente = request.form.get('celular_cliente')  
    
    # Datos incidencia
    
    tipo_incidencia = request.form.get('tipo_incidencia')     
    canal_incidencia = request.form.get('canal_incidencia')     
    asunto_incidencia = request.form.get('asunto_incidencia') 
    detalle_incidencia = request.form.get('detalle_incidencia') 
    
    # Files    
    uploaded_files = request.files.getlist('files')    
    
    logging.debug(f"nombre_cliente {nombre_cliente}")
    logging.debug(f"apellido_cliente {apellido_cliente}")
    logging.debug(f"correo_electronico_cliente {correo_electronico_cliente}")
    logging.debug(f"tipo_documento_cliente {tipo_documento_cliente}")
    logging.debug(f"numero_documento_cliente {numero_documento_cliente}")
    logging.debug(f"celular_cliente {celular_cliente}")
    logging.debug(f"tipo_incidencia {tipo_incidencia}")
    logging.debug(f"canal_incidencia {canal_incidencia}")
    logging.debug(f"asunto_incidencia {asunto_incidencia}")
    logging.debug(f"detalle_incidencia {detalle_incidencia}")
    logging.debug(f"uploaded_files {uploaded_files}")

    validator_incident.validate_incident_data(nombre_cliente,
                                              apellido_cliente, 
                                              correo_electronico_cliente,
                                              tipo_documento_cliente,
                                              numero_documento_cliente,
                                              celular_cliente,
                                              tipo_incidencia,
                                              canal_incidencia,
                                              asunto_incidencia,
                                              detalle_incidencia)
    

    return 'pong', 200