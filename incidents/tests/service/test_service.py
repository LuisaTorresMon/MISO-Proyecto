from datetime import datetime, timedelta

import faker
import pytest
from io import BytesIO
import json
from faker import Faker
from src.main import app
from src.models.models import Incidente, db, Canal, Estado, Tipo 
from src.service.incident_service import IncidentService
from src.service.calls_service import CallsService
from src.service.board_service import BoardService
from google.auth.credentials import AnonymousCredentials 


fake = Faker()       
incident_service = IncidentService()
call_service = CallsService()
board_service = BoardService()

class TestService:

    @pytest.fixture(scope='session', autouse=True)
    def populate_database(self):

        with app.app_context():
        
            canales = [
                Canal(nombre_canal='Llamada Telefónica', precio=10000.0),
                Canal(nombre_canal='Correo Electronico', precio=30000.0),
                Canal(nombre_canal='App Movil', precio=50000.0)
            ]
            db.session.bulk_save_objects(canales)

            tipos = [
                Tipo(tipo='Petición'),
                Tipo(tipo='Queja/Reclamo'),
                Tipo(tipo='Sugerencia')
            ]
            db.session.bulk_save_objects(tipos)

            estados = [
                Estado(estado='Abierto'),
                Estado(estado='Desestimado'),
                Estado(estado='Escalado'),
                Estado(estado='Cerrado Satisfactoriamente'),
                Estado(estado='Cerrado Insatisfactoriamente'),
                Estado(estado='Reaperturado')
            ]
            
            db.session.bulk_save_objects(estados)

            db.session.commit()
        
            yield 
            
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @pytest.fixture 
    def client(self):
      with app.test_client() as client:
        yield client

    
    def test_creacion_incidencia_exitosa_creacion_persona(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.requests.post', return_value=mocker.Mock(status_code=201, json=lambda: {'id': 1}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('src.service.incident_service.publish_ia_request')
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            name = fake.name()
            last_name = fake.name()
            email_client = f"{fake.word()}@outlook.com"
            identity_type = fake.name()
            cellphone = fake.random_number(digits=10)
            identity_number = fake.random_number(digits=10)
            incident_type = 'Petición'
            incident_channel = 'Correo Electronico'
            incident_subject = fake.sentence(nb_words=8)
            incident_detail = fake.sentence(nb_words=8)
            user_id = 1                 

            incident = incident_service.create_incident(
                name, 
                last_name, 
                email_client, 
                identity_type, 
                identity_number, 
                cellphone, 
                incident_type, 
                incident_channel, 
                incident_subject, 
                incident_detail,
                None,
                user_id,
                None,
                token,
                "WEB"
                )            
            
            assert incident is not None  
            
    def test_creacion_incidencia_exitosa_creacion_persona_archivos(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.requests.put', return_value=mocker.Mock(status_code=201, json=lambda: {'id': 1}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('src.service.incident_service.publish_ia_request')

            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            name = fake.name()
            last_name = fake.name()
            email_client = f"{fake.word()}@outlook.com"
            identity_type = fake.name()
            cellphone = fake.random_number(digits=10)
            identity_number = fake.random_number(digits=10)
            incident_type = 'Petición'
            incident_channel = 'Correo Electronico'
            incident_subject = fake.sentence(nb_words=8)
            incident_detail = fake.sentence(nb_words=8)
            user_id = 1 
            person_id = 1
            
            files = [ (BytesIO(b"archivo de prueba"), 'test_file.txt') ]                

            incident = incident_service.create_incident(
                name, 
                last_name, 
                email_client, 
                identity_type, 
                identity_number, 
                cellphone, 
                incident_type, 
                incident_channel, 
                incident_subject, 
                incident_detail,
                files,
                user_id,
                person_id,
                token,
                 "WEB"
                )            
            
            assert incident is not None 
            
    def test_creacion_incidencia_exitosa_actualizacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.requests.put', return_value=mocker.Mock(status_code=201, json=lambda: {'id': 1}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('src.service.incident_service.publish_ia_request')

            mock_response_data = {
                'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
                }
            }

            mocker.patch('src.service.incident_service.requests.get', return_value=mocker.Mock(status_code=201, json=lambda: mock_response_data))
            
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')

            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            name = fake.name()
            last_name = fake.name()
            email_client = f"{fake.word()}@outlook.com"
            identity_type = fake.name()
            cellphone = fake.random_number(digits=10)
            identity_number = fake.random_number(digits=10)
            incident_type = 'Petición'
            incident_channel = 'Correo Electronico'
            incident_subject = fake.sentence(nb_words=8)
            incident_detail = fake.sentence(nb_words=8)
            user_id = 1 
            person_id = 1
            
            files = [ (BytesIO(b"archivo de prueba"), 'test_file.txt') ]                

            incident = incident_service.create_incident(
                name, 
                last_name, 
                email_client, 
                identity_type, 
                identity_number, 
                cellphone, 
                incident_type, 
                incident_channel, 
                incident_subject, 
                incident_detail,
                files,
                user_id,
                person_id,
                token,
                 "WEB"
                )    
            
            status= 2
            observations= fake.name()
            user_creator_id= 2
            user_assigned_to= 2
            
            files: (BytesIO(b"archivo de prueba"), 'test_file.txt')      
            
            incident = incident_service.update_incident(status, observations, user_creator_id, user_assigned_to, files, incident['id'], '')    
            
            assert incident is not None 

    def create_incidents(self, canal_id, estado_id, fecha_creacion, count, codigo, descripcion, asunto, fecha_actualizacion, usuario_creador_id, usuario_asignado_id, persona_id, 
                         tipo_id):
        incidents = [
            Incidente(
                codigo = codigo,
                descripcion = descripcion,
                asunto = asunto,
                fecha_creacion = fecha_creacion,
                fecha_actualizacion = fecha_actualizacion,
                canal_id = canal_id,
                usuario_creador_id = usuario_creador_id,
                usuario_asignado_id = usuario_asignado_id,
                persona_id = persona_id,
                estado_id = estado_id,
                tipo_id = tipo_id
            )
            for _ in range(count)
        ]
        db.session.bulk_save_objects(incidents)
        db.session.commit()

    def test_get_percentage_by_channel_all_channels(self):
        with app.app_context():
            db.session.query(Incidente).delete()
            db.session.commit()

            self.create_incidents(canal_id=1, estado_id=1, fecha_creacion=datetime.now(), count=5, codigo="aa", descripcion="aa", asunto="aa", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=1), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)
            self.create_incidents(canal_id=2, estado_id=1, fecha_creacion=datetime.now(), count=3, codigo="bb", descripcion="bb", asunto="bb", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=1), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)
            self.create_incidents(canal_id=3, estado_id=1, fecha_creacion=datetime.now(), count=2, codigo="cc", descripcion="cc", asunto="cc", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=1), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)

            percentages = board_service.get_percentage_by_channel()
            response_as_dict = json.loads(percentages.response[0].decode('utf-8'))
            response_as_dict['channels'] = sorted(
                [{'channel': c['channel'], 'value': c['value']} for c in
                 response_as_dict['channels']],
                key=lambda x: x['channel']
            )
            expected = {
                'channels': [
                    {'channel': 'App Movil', 'value': 20},
                    {'channel': 'Correo Electrónico', 'value': 30},
                    {'channel': 'Llamada Telefónica', 'value': 50},
                ]
            }

            assert response_as_dict == expected, f"Diferencias encontradas: {response_as_dict} != {expected}"
    
    def test_get_percentage_by_channel_with_canal_filter(self):
        with app.app_context():
            percentages = board_service.get_percentage_by_channel(canal_id=1)
            response_as_dict = percentages.get_json()
            exist_call = any(channel['channel'] == 'Llamada Telefónica' for channel in response_as_dict['channels'])
            assert exist_call
            total_value = sum(channel['value'] for channel in response_as_dict['channels'])
            assert total_value == 50
    
    def test_get_percentage_by_channel_with_estado_filter(self):
        with app.app_context():
            self.create_incidents(canal_id=1, estado_id=2, fecha_creacion=datetime.now(), count=5, codigo="aa", descripcion="aa", asunto="aa", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=1), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)

            percentages = board_service.get_percentage_by_channel(estado_id=2)
            response_as_dict = percentages.get_json()
            exist_call = any(channel['channel'] == 'Llamada Telefónica' for channel in response_as_dict['channels'])
            assert exist_call
            total_value = sum(channel['value'] for channel in response_as_dict['channels'])
            assert total_value == 100
    
    def test_get_percentage_by_channel_with_date_range(self):
        with app.app_context():
            fecha_inicio = datetime.now() - timedelta(days=1)
            fecha_fin = datetime.now()

            self.create_incidents(canal_id=1, estado_id=1, fecha_creacion=fecha_inicio + timedelta(hours=1), count=5, codigo="aa", descripcion="aa", asunto="aa", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=3), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)
            self.create_incidents(canal_id=2, estado_id=1, fecha_creacion=fecha_inicio - timedelta(days=1), count=3, codigo="bb", descripcion="bb", asunto="bb", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=3), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)

            percentages = board_service.get_percentage_by_channel(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            response_as_dict = percentages.get_json()
            exist_call = any(channel['channel'] == 'Llamada Telefónica' for channel in response_as_dict['channels'])
            assert exist_call

    def test_get_percentage_by_channel_with_combined_filters(self):
        with app.app_context():
            fecha_inicio = datetime.now() - timedelta(days=1)
            fecha_fin = datetime.now()

            self.create_incidents(canal_id=1, estado_id=1, fecha_creacion=fecha_inicio + timedelta(hours=1), count=3, codigo="aa", descripcion="aa", asunto="aa", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=3), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)
            self.create_incidents(canal_id=1, estado_id=2, fecha_creacion=fecha_inicio + timedelta(hours=1), count=2, codigo="bb", descripcion="bb", asunto="bb", 
                                  fecha_actualizacion=datetime.now() + timedelta(hours=3), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)

            percentages = board_service.get_percentage_by_channel(canal_id=1, estado_id=1, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            response_as_dict = percentages.get_json()
            exist_call = any(channel['channel'] == 'Llamada Telefónica' for channel in response_as_dict['channels'])
            assert exist_call
            total_value = sum(channel['value'] for channel in response_as_dict['channels'])
            assert total_value == 72
    
    def test_get_summarized_incidents_all(self):
        with app.test_client() as test_client:
            db.session.query(Incidente).delete()
            db.session.commit()

            self.create_incidents(canal_id=1, estado_id=1, fecha_creacion=datetime.now() - timedelta(days=2), count=1, codigo="aa", descripcion="aa", asunto="aa", 
                                  fecha_actualizacion=datetime.now() - timedelta(days=1), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)
            self.create_incidents(canal_id=2, estado_id=2, fecha_creacion=datetime.now() - timedelta(days=5), count=1, codigo="bb", descripcion="bb", asunto="bb", 
                                  fecha_actualizacion=datetime.now() - timedelta(days=4), usuario_creador_id=1, usuario_asignado_id=1, persona_id=1, tipo_id=1)
            
            response = board_service.get_summarized_incidents()
            data = response.get_json()
            
            assert response.status_code == 200
            assert data['total'] == 2
            assert all("id" in incident for incident in data['incidentes'])
    
    def test_get_summarized_incidents_with_canal_filter(self):
        with app.test_client() as test_client:
            response = board_service.get_summarized_incidents(canal_id=1)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['canal'] == 'Llamada Telefónica'
    
    def test_get_summarized_incidents_with_estado_filter(self):
        with app.test_client() as test_client:
            response = board_service.get_summarized_incidents(estado_id=2)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['estado'] == 'Desestimado'

    def test_get_summarized_incidents_with_date_range(self):
        fecha_inicio = datetime.now() - timedelta(days=6)
        fecha_fin = datetime.now() - timedelta(days=3)

        with app.test_client() as test_client:
            response = board_service.get_summarized_incidents(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['canal'] == 'Correo Electrónico'
    
    def test_get_summarized_incidents_with_combined_filters(self):
        fecha_inicio = datetime.now() - timedelta(days=10)
        fecha_fin = datetime.now()

        with app.test_client() as test_client:
            response = board_service.get_summarized_incidents(canal_id=1, estado_id=1, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['canal'] == 'Llamada Telefónica'
            assert data['incidentes'][0]['estado'] == 'Abierto'

    def test_get_user_ia_by_username_success(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=200, json=lambda: mock_response_data))

        user_ia = incident_service.get_user_ia_by_username()

        assert user_ia is not None

    def test_get_user_ia_by_username_fail(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=400, json=lambda: mock_response_data))

        user_ia = incident_service.get_user_ia_by_username()

        assert user_ia is None

    def test_get_user_by_username_fail(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=400, json=lambda: mock_response_data))

        user = incident_service.get_user_by_username(fake.word(), fake.user_name())

        assert user is None

    def test_get_user_by_username_success(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=200, json=lambda: mock_response_data))

        user = incident_service.get_user_by_username(fake.word(), fake.user_name())

        assert user is not None

    def test_get_user_success(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=200, json=lambda: mock_response_data))

        user = incident_service.get_user(fake.word(), fake.random_number())

        assert user is not None

    def test_get_person_success(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=200, json=lambda: mock_response_data))

        user = incident_service.get_person(fake.word(), fake.random_number())

        assert user is not None

    def test_get_person_fail(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=400, json=lambda: mock_response_data))

        user = incident_service.get_person(fake.word(), fake.random_number())

        assert user is None

    def test_get_person_by_id_success(self, mocker):
        mock_response_data = {
            'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
            }
        }

        mocker.patch('src.service.incident_service.requests.get',
                     return_value=mocker.Mock(status_code=200, json=lambda: mock_response_data))

        user = incident_service.get_person_by_id(fake.random_number(), fake.word())

        assert user is not None