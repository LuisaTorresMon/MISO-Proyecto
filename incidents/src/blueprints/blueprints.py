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
    headers = request.headers
    token_encabezado = headers.get('Authorization')
    logging.debug(token_encabezado)

    # Datos cliente
    person_id = request.form.get('person_id') 
    name_person = request.form.get('name')     
    lastname_person = request.form.get('lastName')     
    email_person = request.form.get('emailClient') 
    identity_type_person = request.form.get('identityType')     
    identity_number_person = request.form.get('identityNumber')  
    cellphone_person = request.form.get('cellPhone')  
    
    # Datos incidencia  
    user_id = request.form.get('user_id')
    incident_type = request.form.get('incidentType')     
    channel_incident = request.form.get('incidentChannel')     
    subject_incident = request.form.get('incidentSubject') 
    detail_incident = request.form.get('incidentDetail') 
    
    # Files    
    uploaded_files = request.files.getlist('files')    
    
    logging.debug(f"name_person {name_person}")
    logging.debug(f"lastname_person {lastname_person}")
    logging.debug(f"email_person {email_person}")
    logging.debug(f"identity_type_person {identity_type_person}")
    logging.debug(f"identity_number_person {identity_number_person}")
    logging.debug(f"cellphone_person {cellphone_person}")
    logging.debug(f"incident_type {incident_type}")
    logging.debug(f"channel_incident {channel_incident}")
    logging.debug(f"subject_incident {subject_incident}")
    logging.debug(f"detail_incident {detail_incident}")
    logging.debug(f"uploaded_files {uploaded_files}")
    
    logging.debug(f"user_id {user_id}")
    logging.debug(f"person_id {person_id}")


    validator_incident.validate_incident_data(name_person,
                                              lastname_person, 
                                              email_person,
                                              identity_type_person,
                                              identity_number_person,
                                              cellphone_person,
                                              incident_type,
                                              channel_incident,
                                              subject_incident,
                                              detail_incident,
                                              token_encabezado)
    
    
    incident = incident_service.create_incident(name_person,
                                              lastname_person, 
                                              email_person,
                                              identity_type_person,
                                              identity_number_person,
                                              cellphone_person,
                                              incident_type,
                                              channel_incident,
                                              subject_incident,
                                              detail_incident,
                                              uploaded_files,
                                              user_id,
                                              person_id,
                                              token_encabezado)

    return incident, 201

@incident_blueprint.route('/calls/<int:id>', methods=['GET'])
def find_calls_by_person(id):
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(token_encabezado)
         
        validator_incident.validate_token_sent(token_encabezado)
        validator_incident.valid_token(token_encabezado)
         
        return call_service.find_calls_by_person(id)
    except Exception as err:
        raise ServerSystemException(f"Error a la hora de conultar las llamadas del usuario {err}, porfavor contacte con su administrador")
    
@incident_blueprint.route('/person/<int:id>', methods=['GET'])
def find_incidents_by_person(id):
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(token_encabezado)
         
        validator_incident.validate_token_sent(token_encabezado)
        validator_incident.valid_token(token_encabezado)
        
        return incident_service.find_incidents_by_person(id)
    except Exception as err:
        logging.debug(err)
        raise ServerSystemException(f"Error a la hora de conultar las llamadas del usuario {err}, porfavor contacte con su administrador")
    
@incident_blueprint.route('/all', methods=['GET'])
def find_incidents():
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(token_encabezado)
         
        validator_incident.validate_token_sent(token_encabezado)
        validator_incident.valid_token(token_encabezado)
        
        return incident_service.find_incidents(token_encabezado)
    except Exception as err:
        logging.debug(err)
        raise ServerSystemException(f"Error a la hora de conultar las incidencias {err}, porfavor contacte con su administrador")
  
@incident_blueprint.route('/history/<int:id_incident>', methods=['GET'])
def find_history_by_incident(id_incident):
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(token_encabezado)
         
        validator_incident.validate_token_sent(token_encabezado)
        validator_incident.valid_token(token_encabezado)
        
        logging.debug(f"id_incident {id_incident}")
        
        return incident_service.find_history_by_incident(token_encabezado, id_incident)
    except Exception as err:
        logging.debug(err)
        raise ServerSystemException(f"Error a la hora de conultar las incidencias {err}, porfavor contacte con su administrador")
   
    
@incident_blueprint.route('/get/<int:id>', methods=['GET'])
def find_incident_by_id(id):
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(token_encabezado)
         
        validator_incident.validate_token_sent(token_encabezado)
        validator_incident.valid_token(token_encabezado)
        
        return incident_service.find_incident_by_id(id, token_encabezado)
    except Exception as err:
        logging.debug(f"excepcion {err}")
        raise ServerSystemException(f"Error a la hora de conultar el detalle de la incidencia {err}, porfavor contacte con su administrador")
    
@incident_blueprint.route('/call/<int:id>', methods=['GET'])
def find_call_by_id(id):
    try:
        headers = request.headers
        token_encabezado = headers.get('Authorization')
        logging.debug(token_encabezado)
         
        validator_incident.validate_token_sent(token_encabezado)
        validator_incident.valid_token(token_encabezado)
        
        return call_service.get_call_by_id(id)
    except Exception as err:
        logging.debug(f"excepcion {err}")
        raise ServerSystemException(f"Error a la hora de conultar el detalle de la incidencia {err}, porfavor contacte con su administrador")
    