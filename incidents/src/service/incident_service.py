from ..models.models import Incidente, IncidenteSchema, EvidenciaHistorico, EvidenciaHistoricoSchema, HistoricoIncidencia, HistoricoIncidenciaSchema, Evidencia, EvidenciaSchema, Canal, Tipo, Estado, HistoricoIncidencia, db 
from .calls_service import CallsService
from ..utils.utils import CommonUtils
from ..errors.errors import ServerSystemException
from datetime import datetime
from tinytag import TinyTag
from dotenv import load_dotenv
import random, logging, os
import requests
import copy

incident_schema = IncidenteSchema()
calls_service = CallsService()
common_utils = CommonUtils()
history_evidencie_schemma = EvidenciaHistoricoSchema()
history_schema = HistoricoIncidenciaSchema()
evidence_schema = EvidenciaSchema()

load_dotenv('.env.template')            
USER_URL = os.environ.get('USER_PATH')

class IncidentService():
    
        def create_incident(self, 
                         name_person, 
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
                         token):
            
            person = {
                "name": name_person,
                "lastname": lastname_person,
                "email": email_person,
                "identity_type": identity_type_person,
                "identity_number": identity_number_person,
                "cellphone": cellphone_person 
            }
            
            if not person_id:
                person_id = self.create_person(token, person)
            else: 
                self.update_person(token, person)
                
            incident = self.save_incident(incident_type,
                              channel_incident,
                              subject_incident,
                              detail_incident,
                              user_id,
                              person_id)
           
            self.save_incident_history(incident, f" Se ha creado la incidencia {incident.codigo} con éxito", user_id)
            
            if channel_incident == 'Llamada Telefónica':
                calls_service.save_call_incidence(incident, user_id, person_id)
                
            if uploaded_files:
               self.save_upload_files(uploaded_files, incident, user_id)
           
            return incident_schema.dump(incident)
        
        def update_incident(self, status, 
                            observations, 
                            user_creator_id, 
                            user_assigned_id,
                            uploaded_files, 
                            incident_id,
                            token):
            
           incident = db.session.query(Incidente).filter(Incidente.id == incident_id).first()
           last_status = incident.estado.estado          
           if(incident.estado_id != int(status)):
                incident.estado_id = status   
                db.session.commit()

                self.save_incident_history(incident, f"Se ha cambiado el estado de la incidencia de {last_status} a {incident.estado.estado}", user_creator_id)
           
           if(incident.usuario_asignado_id != int(user_assigned_id)):
               
                last_assigned_user = self.get_user(token, incident.usuario_asignado_id)
                new_assigned_user = self.get_user(token, user_assigned_id)
               
                incident.usuario_asignado_id = user_assigned_id   
                db.session.commit()
                
                if(last_assigned_user and new_assigned_user):
                    self.save_incident_history(incident, f"Se ha cambiado el usuario asignado de la incidencia de {last_assigned_user['persona']['nombres']} {last_assigned_user['persona']['apellidos']} a {new_assigned_user['persona']['nombres']} {new_assigned_user['persona']['apellidos']}", user_creator_id)

           
           if(observations):
                self.save_incident_history(incident, f"Se agrega el comentario {observations}", user_creator_id)
                
           if(uploaded_files and len(uploaded_files)):
                self.save_upload_files(uploaded_files, incident, user_creator_id)

           return incident_schema.dump(incident)

       
        def save_incident(self, 
                         incident_type,
                         channel_incident,
                         subject_incident,
                         detail_incident,
                         user_id,
                         person_id):
            
              logging.debug("Iniciando el guardado de la incidencia")

              canal = self.get_canal_by_nombre(channel_incident);
              tipo = self.get_tipo_by_nombre(incident_type);
              estado = self.get_estado_by_nombre('Abierto');
              
              incident_code = self.generate_incident_code()
              logging.debug(f"incident {incident_code}")
              
              incident = Incidente(
                  codigo = incident_code,
                  descripcion = detail_incident,
                  asunto = subject_incident,
                  canal_id = canal.id,
                  tipo_id = tipo.id,
                  estado_id =  estado.id,
                  usuario_creador_id = user_id,
                  usuario_asignado_id = user_id,
                  persona_id = person_id
              )
              
              db.session.add(incident)
              db.session.commit()
                            
              return incident
          
        def create_person(self, token, person):
            
            url = f"{USER_URL}/person/create"

            headers = common_utils.obtener_token(token)

            response = requests.post(url, headers=headers, json=person)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 201:
                
                logging.debug(f"response.json() {response.json()}")
                person_created = response.json()
                return person_created.get('id')
            else:
                raise ServerSystemException
                
        def update_person(self, token, person):
            
            url = f"{USER_URL}/person/create"
            headers = common_utils.obtener_token(token)

            response = requests.put(url, headers=headers, json=person)
            logging.debug(f"codigo de respuesta {response.text}")
        
        def generate_incident_code(self):
             random_number = random.randint(1, 5000)
             incident_code = f"INC{random_number:05d}"
        
             logging.debug(f"incident code {incident_code}")
             
             return incident_code       
            
        def save_upload_files(self, uploaded_files, incident, user_creator_id):
            
            try:
                logging.debug("Iniciando el guardado de los archivos adjuntos")
            
                files_name = [file.filename for file in uploaded_files]
                files_name_contact = ', '.join(files_name)
            
                logging.debug(f" nombre concatenado {files_name_contact}")

                incident_history = self.save_incident_history(incident, f" El usuario prueba ha añadido los archivos {files_name_contact} a la incidencia {incident.codigo}", user_creator_id)
            
                for file in uploaded_files:
                    file_name = file.filename
                    logging.debug(f"nombre_archivo {file_name}")
                
                    file_ext = file.mimetype
                    logging.debug(f"formato_archivo {file_ext}")
                
                    file.seek(0, 2)
                    file_size = file.tell()
                    file.seek(0)
                    logging.debug(f"file_size {file_size}")
                    
                    common_utils.upload_file_to_gcs_by_file(file, f"incident-files/{file.filename}")
                
                    evidence = self.save_evidence_database(file_name, file_ext, file_size, incident)
                    self.save_evidence_history(evidence, incident_history)
            except Exception as err:
                logging.debug(f"error a la hora de crear los archivos {err}")
                
        def save_evidence_history(self, evidence, incident_history):
            try:
                evidence_history = EvidenciaHistorico(
                    evidencia_id = evidence.id,
                    historico_id = incident_history.id
                )
            
                db.session.add(evidence_history)
                db.session.commit()                
            except Exception as err:
                logging.debug(f"error a la hora de crear el evidence history {err}")

        def save_incident_history(self, incident, comments, user_creator_id):
            
            incident_history = None
            try: 
                logging.debug("Iniciando el guardado de la historia de la incidencia")
            
                incident_history = HistoricoIncidencia(
                    observaciones = comments,
                    incidencia_id = incident.id,
                    usuario_creador_id = user_creator_id,
                    estado_id = incident.estado_id,
                    usuario_asignado_id = incident.usuario_asignado_id
                )
            
                db.session.add(incident_history)
                db.session.commit()   
            
            except Exception as err:
                logging.debug(f"error a la hora de crear el evidence history {err}")
            
            return incident_history

        def save_evidence_database(self, file_name, file_ext, file_size, incident):
            evidence = None
            
            try: 

                logging.debug("Iniciando el guardado de las evidencia en base de datos")
            
                evidence = Evidencia(
                    nombre_adjunto = file_name,
                    formato = file_ext,
                    tamano = file_size,
                    incidencia_id = incident.id
                )
            
                db.session.add(evidence)
                db.session.commit()
            except Exception as err:
                logging.debug(f"error a la hora de guardar archivos en bd {err}")
            
            return evidence
        
        def find_incidents_by_person(self,id_person):
           incidents = db.session.query(Incidente).filter_by(persona_id = id_person).all()
           incidents_schema = []

           for incident in incidents:
               incident_data = incident_schema.dump(incident)  
               incident_data['estado_nombre'] = incident.estado.estado  
               incidents_schema.append(incident_data)
                          
           return incidents_schema
       
        def find_incidents(self, token):
           incidents = db.session.query(Incidente).all()
           incidents_schema = []

           for incident in incidents:
               incident_data = incident_schema.dump(incident)  
               person = self.get_person(token, incident.persona_id)
               if person:
                  incident_data['person'] = person
               incidents_schema.append(incident_data)
                          
           return incidents_schema
       
        def find_history_by_incident(self, token, id_incident):
           histories = db.session.query(HistoricoIncidencia).filter(HistoricoIncidencia.incidencia_id == id_incident).all()

           histories_schema = []
           for history in histories:
               history_data = history_schema.dump(history)
               
               user = self.get_user(token, history.usuario_creador_id)
               history_data['usuario_creador'] = user
               
               evidences_history = db.session.query(EvidenciaHistorico).filter(EvidenciaHistorico.historico_id == history.id).all()
               evidencias_schema = []
               
               for evidence_history in evidences_history:
                   if evidence_history.evidencia:
                       evidence = evidence_schema.dump(evidence_history.evidencia)
                       evidencias_schema.append(evidence)  
                                  
               history_data['evidence'] = evidencias_schema
               histories_schema.append(history_data)
                          
           return histories_schema
                                 
        def find_incident_by_id(self, id, token):
            
            logging.debug(f"id incidencia {id}")
            incident = db.session.query(Incidente).filter_by(id=id).first()

            logging.debug(f"incident {incident}")
            incident_data = incident_schema.dump(incident)  
            person = self.get_person(token, incident.persona_id)
            asigned_user = self.get_user(token, incident.usuario_asignado_id)

            if person:
                incident_data['person'] = person
            if asigned_user:
                incident_data['usuario_asignado'] = asigned_user
                          
            return incident_data
        
        def get_person(self, token, id):
            
            url = f"{USER_URL}/person/{id}"

            headers = common_utils.obtener_token(token)

            response = requests.get(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 200: 
                logging.debug(f"response.json() {response.json()}") 
                return response.json()
            else:
                return None
            
        def get_user(self, token, id):
            
            url = f"{USER_URL}/get/{id}"

            headers = common_utils.obtener_token(token)

            response = requests.get(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 200: 
                logging.debug(f"response.json() {response.json()}") 
                return response.json()
            else:
                return None
       
        def get_canal_by_nombre(self, channel_incident):
            return db.session.query(Canal).filter_by(nombre_canal = channel_incident).first()
    
        def get_tipo_by_nombre(self, incident_type):
            return db.session.query(Tipo).filter_by(tipo = incident_type).first()
    
        def get_estado_by_nombre(self, estado_incidencia):
            return db.session.query(Estado).filter_by(estado = estado_incidencia).first() 