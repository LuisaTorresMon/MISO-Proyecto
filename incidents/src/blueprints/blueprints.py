from flask import Blueprint, request, jsonify
from ..validations.validations import ValidatorIncidents
from ..service.incident_service import IncidentService
from ..service.calls_service import CallsService
from ..errors.errors import ServerSystemException
import logging, os

incident_blueprint = Blueprint('incident', __name__)
validator_incident = ValidatorIncidents()
incident_service = IncidentService()
call_service = CallsService()

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
    
    
    incident = incident_service.create_incident(nombre_cliente,
                                              apellido_cliente, 
                                              correo_electronico_cliente,
                                              tipo_documento_cliente,
                                              numero_documento_cliente,
                                              celular_cliente,
                                              tipo_incidencia,
                                              canal_incidencia,
                                              asunto_incidencia,
                                              detalle_incidencia,
                                              uploaded_files)

    return incident, 201

@incident_blueprint.route('/calls/<int:id>', methods=['GET'])
def find_calls_by_person(id):
    try:
        return call_service.find_calls_by_person(id)
    except Exception as err:
        raise ServerSystemException(f"Error a la hora de conultar las llamadas del usuario {err}, porfavor contacte con su administrador")
    
@incident_blueprint.route('/person/<int:id>', methods=['GET'])
def find_incidents_by_person(id):
    try:
        return incident_service.find_incidents_by_person(id)
    except Exception as err:
        raise ServerSystemException(f"Error a la hora de conultar las llamadas del usuario {err}, porfavor contacte con su administrador")
    
    