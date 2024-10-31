import pytest
from io import BytesIO
from faker import Faker
from src.main import app
from src.models.models import db, Canal, Estado, Tipo 
from src.service.incident_service import IncidentService
from src.service.calls_service import CallsService
from google.auth.credentials import AnonymousCredentials 


fake = Faker()       
incident_service = IncidentService()
call_service = CallsService()

class TestService():

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
                token
                )            
            
            assert incident is not None  
            
    def test_creacion_incidencia_exitosa_creacion_persona_archivos(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.requests.put', return_value=mocker.Mock(status_code=201, json=lambda: {'id': 1}))
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
                token
                )            
            
            assert incident is not None 
            
    def test_creacion_incidencia_exitosa_actualizacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.requests.put', return_value=mocker.Mock(status_code=201, json=lambda: {'id': 1}))
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
                token
                )    
            
            status= 2
            observations= fake.name()
            user_creator_id= 2
            user_assigned_to= 2
            
            files: (BytesIO(b"archivo de prueba"), 'test_file.txt')      
            
            incident = incident_service.update_incident(status, observations, user_creator_id, user_assigned_to, files, incident['id'], '')    
            
            assert incident is not None 