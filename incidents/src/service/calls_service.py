from ..models.models import Llamada, LlamadaSchema, db
from tinytag import TinyTag
from datetime import datetime
import logging, random, os
from ..utils.utils import CommonUtils

calls_schema = LlamadaSchema()
common_utils = CommonUtils()

class CallsService():

        def save_call_incidence(self, incident, user_id, person_id):
            
            logging.debug("Iniciando el guardado de la llamada")

            current_date = datetime.now()
            
            audios_random = random.randint(0, 1)
            audios_name = ['llamada_1.mp3', 'llamada_2.mp3']
            logging.debug(audios_name)
            
            audio_name = audios_name[audios_random]
            audio_path = os.path.join('audios', audio_name)

            audio = TinyTag.get(audio_path)

            common_utils.upload_file_to_gcs_by_path(audio_path, f"incident-calls/{audio_name}_{incident.codigo}_{current_date}")

            incident_call = Llamada(
                nombre_grabacion = f"{audio_name}_{incident.codigo}_{current_date}",
                duracion = f"{audio.duration:.2f}",
                incidencia_id = incident.id,
                usuario_id = user_id,
                persona_id = person_id
            )
        
            db.session.add(incident_call)
            db.session.commit()
            
        def find_calls_by_person(self, id_person):
           calls = db.session.query(Llamada).filter_by(persona_id = id_person).all()
           calls_schema_person = [calls_schema.dump(call) for call in calls]
           
           return calls_schema_person
       
        def get_call_by_id(self, id): 
            call = db.session.query(Llamada).filter_by(id=id).first()
            return calls_schema.dump(call)
        
        