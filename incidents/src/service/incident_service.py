from ..models.models import Incidente, IncidenteSchema, Canal, Tipo, Estado, Evidencia, HistoricoIncidencia, EvidenciaHistorico, db 
from .calls_service import CallsService
from ..utils.utils import CommonUtils
from datetime import datetime
from tinytag import TinyTag
import random, logging, os

incident_schema = IncidenteSchema()
calls_service = CallsService()
common_utils = CommonUtils()

class IncidentService():
    
        def create_incident(self, 
                         nombre_cliente, 
                         apellido_cliente, 
                         correo_electronico_cliente, 
                         tipo_documento_cliente,
                         numero_documento_cliente,
                         celular_cliente,
                         tipo_incidencia,
                         canal_incidencia,
                         asunto_incidencia,
                         detalle_incidencia,
                         uploaded_files):
           
            incident = self.save_incident(tipo_incidencia,
                              canal_incidencia,
                              asunto_incidencia,
                              detalle_incidencia)
           
            self.save_incident_history(incident, f" El usuario prueba ha creado la incidencia {incident.codigo} con éxito")

            calls_service.save_call_incidence(incident)
            if uploaded_files:
               self.save_upload_files(uploaded_files, incident)
           
            return incident_schema.dump(incident)
       
        def save_incident(self, 
                         tipo_incidencia,
                         canal_incidencia,
                         asunto_incidencia,
                         detalle_incidencia):
            
              logging.debug("Iniciando el guardado de la incidencia")

              canal = self.get_canal_by_nombre(canal_incidencia);
              tipo = self.get_tipo_by_nombre(tipo_incidencia);
              estado = self.get_estado_by_nombre('Abierto');
              
              incident_code = self.generate_incident_code()
              logging.debug(f"incident {incident_code}")
              
              incident = Incidente(
                  codigo = incident_code,
                  descripcion = detalle_incidencia,
                  asunto = asunto_incidencia,
                  canal_id = canal.id,
                  tipo_id = tipo.id,
                  estado_id =  estado.id,
                  usuario_creador_id = 1,
                  usuario_asignado_id = 1,
                  persona_id = 1
              )
              
              db.session.add(incident)
              db.session.commit()
                            
              return incident

        
        def generate_incident_code(self):
             random_number = random.randint(1, 5000)
             incident_code = f"INC{random_number:05d}"
        
             logging.debug(f"incident code {incident_code}")
             
             return incident_code     
            
        def save_upload_files(self, uploaded_files, incident):
            
            try:
                logging.debug("Iniciando el guardado de los archivos adjuntos")
            
                files_name = [file.filename for file in uploaded_files]
                files_name_contact = ', '.join(files_name)
            
                logging.debug(f" nombre concatenado {files_name_contact}")

                incident_history = self.save_incident_history(incident, f" El usuario prueba ha añadido los archivos {files_name_contact} a la incidencia {incident.codigo}")
            
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

        def save_incident_history(self, incident, comments):
            
            incident_history = None
            try: 
                logging.debug("Iniciando el guardado de la historia de la incidencia")
            
                incident_history = HistoricoIncidencia(
                    observaciones = comments,
                    incidencia_id = incident.id,
                    usuario_creador_id = 1,
                    estado_id = incident.estado_id,
                    usuario_asignado_id = 1
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
        
        def find_incidents_by_person(self, id_person):
           incidents = db.session.query(Incidente).filter_by(persona_id = id_person).all()
           incidents_schema = [incident_schema.dump(incident) for incident in incidents]
           
           return incidents_schema
       
        def get_canal_by_nombre(self, canal_incidencia):
            return db.session.query(Canal).filter_by(nombre_canal = canal_incidencia).first()
    
        def get_tipo_by_nombre(self, tipo_incidencia):
            return db.session.query(Tipo).filter_by(tipo = tipo_incidencia).first()
    
        def get_estado_by_nombre(self, estado_incidencia):
            return db.session.query(Estado).filter_by(estado = estado_incidencia).first()