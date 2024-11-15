import json
import pytest
from faker import Faker
from src.main import app
from src.models.models import Incidente, db, Canal, Estado, Tipo 
from google.auth.credentials import AnonymousCredentials 
from datetime import datetime, timedelta
from io import BytesIO

fake = Faker()       
        
class TestBlueprints:
    
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
    
    def test_campos_sin_nombre_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'cellPhone': "3142980620",
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo nombre esta vacio, recuerda que es obligatorio'
            
    def test_campos_sin_apellido_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'cellPhone': "3142980620",
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo apellido esta vacio, recuerda que es obligatorio'
            
    def test_campos_sin_email_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'identityType': fake.name(),
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'cellPhone': "3142980620",
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo correo electronico esta vacio, recuerda que es obligatorio'
            
    def test_campos_sin_tipo_identificacion_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'cellPhone': "3142980620",
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo tipo de documento esta vacio, recuerda que es obligatorio'
            
    def test_campos_sin_numero_identificacion_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'cellPhone': "3142980620",
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo numero de documento esta vacio, recuerda que es obligatorio'
            
    def test_campos_sin_telefono_identificacion_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo celular esta vacio, recuerda que es obligatorio'
            
    def test_campos_sin_canal_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': 'test@gmail.com',
                    'identityType': fake.name(),
                    'cellPhone': '3142980620',
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo canal de incidente esta vacio, recuerda que es obligatorio'        
            
    def test_campos_sin_titulo_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'cellPhone': "3142980620",
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentDetail': fake.sentence(nb_words=8)
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo asunto de incidente esta vacio, recuerda que es obligatorio'        
            
    def test_campos_sin_detalle_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'cellPhone': "3142980620",
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8)                    
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El campo detalle de incidente esta vacio, recuerda que es obligatorio'        
            
    def test_campos_numero_documento_invalido_cc_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': 'Cédula_Cuidadania',
                    'cellPhone': "3142980620",
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)                 
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El numero de documento cuando es de tipo Cedula de cuidadania, debe ser numerico y debe tener una longitud de 8 0 10 caracteres'        
                    
    def test_campos_numero_documento_invalido_ce_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': 'Cédula_Extrangeria',
                    'cellPhone': "3142980620",
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)                 
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El numero de documento cuando es de tipo Cedula de extranjeria, debe ser numerico y debe tener una longitud de 12 caracteres'        
                    
    def test_campos_telefono_invalido_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': "test@gmail.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.name(),
                    'identityNumber': fake.pystr(min_chars=2, max_chars=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)                 
                    }
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El celular debe ser un campo numerico'        
    
    def test_campos_email_invalido_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': fake.name(),
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': fake.name(),
                    'incidentChannel': fake.word(),
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8)                 
                    }
            
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 400 and incident_data.get('msg') == 'El correo electronico debe ser un correo valido'        
    
    
    def test_creacion_incidencia_sin_token(self):
        with app.test_client() as test_client:
     
            incidencia = test_client.post('/incident/create')
            assert incidencia.status_code == 403
            
    def test_creacion_incidencia_token_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3fake"}
     
            incidencia = test_client.post('/incident/create', headers=headers)
            assert incidencia.status_code == 401
          
    def test_creacion_incidencia_exitosa_creacion_persona(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.create_person', return_value=1)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Correo Electronico',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1                 
                    }
            
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 201        
    
    def test_creacion_incidencia_exitosa_con_archivos(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.cloud.storage.Client')

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Correo Electronico',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1,
                    'person_id': 1              
                    }
            
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 201   
            
    def test_creacion_incidencia_exitosa_carga_archivos_llamada(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            file_data = {
                'files': (BytesIO(b"archivo de prueba"), 'test_file.txt')  
            }
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Llamada Telefónica',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1,
                    'person_id': 1              
                    }
            
            form_data.update(file_data)
            
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)

            assert response_service.status_code == 201
            
    def test_creacion_incidencia_exitosa_y_consulta_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
               
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Correo Electronico',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1,
                    'person_id': 1              
                    }
                        
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)
            
            response_service = test_client.get('/incident/person/1', headers=headers)

            assert response_service.status_code == 200
            
    def test_creacion_incidencia_exitosa_y_consulta_llamada_por_persona(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            file_data = {
                'files': (BytesIO(b"archivo de prueba"), 'test_file.txt')  
            }
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Llamada Telefónica',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1,
                    'person_id': 1              
                    }
            
            form_data.update(file_data)
            
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)
            
            response_service = test_client.get('/incident/calls/1', headers=headers)

            assert response_service.status_code == 200
            
    def test_creacion_incidencia_exitosa_y_consulta_llamada_por_persona(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            file_data = {
                'files': (BytesIO(b"archivo de prueba"), 'test_file.txt')  
            }
            
            form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Llamada Telefónica',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1,
                    'person_id': 1              
                    }
            
            form_data.update(file_data)
            
            print(form_data)
            
            response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
            incident_data = response_service.get_json()
            
            print(incident_data)
            
            response_service = test_client.get('/incident/calls/1', headers=headers)
            response_data = response_service.get_json()

            response_service = test_client.get(f"/incident/call/{response_data[0]['id']}", headers=headers)


            assert response_service.status_code == 200
            
    def test_creacion_incidencia_exitosa_y_consulta_total_de_incidentes(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.service.incident_service.IncidentService.get_person', return_value=1)

            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')
            
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            self.create_incident(test_client, headers)
            
            response_service = test_client.get('/incident/all', headers=headers)
            response_data = response_service.json
            
            assert response_service.status_code == 200
            assert len(response_data) > 0
            
    def test_creacion_incidencia_exitosa_y_consulta_incidente_por_id(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.service.incident_service.IncidentService.get_person', return_value=1)
            mocker.patch('src.service.incident_service.IncidentService.get_user', return_value=1)

            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')
            
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            incident_data = self.create_incident(test_client, headers)
            
            response_service = test_client.get(F"/incident/get/{incident_data['id']}", headers=headers)
            response_data = response_service.json
            
            assert response_service.status_code == 200
            assert response_data['id'] == incident_data['id']
            
    def test_creacion_incidencia_exitosa_y_consulta_incidente_historia_por_id(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mocker.patch('src.service.incident_service.IncidentService.get_person', return_value=1)
            mocker.patch('src.service.incident_service.IncidentService.get_user', return_value=1)

            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')
            
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            incident_data = self.create_incident(test_client, headers)
            
            response_service = test_client.get(F"/incident/history/{incident_data['id']}", headers=headers)
            response_data = response_service.json
            
            assert response_service.status_code == 200
            assert len(response_data) > 0
            
    def test_creacion_incidencia_exitosa_y_actualizacion_incidencia_por_id(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.service.incident_service.IncidentService.update_person', return_value=1)
            mock_response_data = {
                'persona': {
                'apellidos': 'ApellidoAntiguo',
                'nombres': 'NombreNuevo'
                }
            }

            mocker.patch('src.service.incident_service.IncidentService.get_user', return_value=mock_response_data)
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: mock_response_data))
            mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
            mocker.patch('google.cloud.storage.Client')
            
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            incident_data = self.create_incident(test_client, headers)
            
            file_data = {
                'files': (BytesIO(b"archivo de prueba"), 'test_file.txt')  
            }
            
            form_data = {'status': 2,
                        'observations': fake.name(),
                        'userCreatorId': 2,
                        'assignedTo': 2}
            
            form_data.update(file_data)

            response_service = test_client.put(F"/incident/update/{incident_data['id']}", data=form_data, headers=headers, content_type='multipart/form-data')
            
            assert response_service.status_code == 201
            
    def create_incident(self, test_client, headers):   
                    
        form_data = {'name': fake.name(),
                    'lastName': fake.name(),
                    'emailClient': f"{fake.word()}@outlook.com",
                    'identityType': fake.name(),
                    'cellPhone': fake.random_number(digits=10),
                    'identityNumber': fake.random_number(digits=10),
                    'incidentType': 'Petición',
                    'incidentChannel': 'Correo Electronico',
                    'incidentSubject': fake.sentence(nb_words=8),
                    'incidentDetail': fake.sentence(nb_words=8),
                    'user_id': 1,
                    'person_id': 1              
                    }
                        
        print(form_data)
            
        response_service = test_client.post('/incident/create',data=form_data, headers=headers, content_type='multipart/form-data')
        incident_data = response_service.get_json()
            
        print(incident_data)
        
        return incident_data
    
    def test_get_percentage_of_incidents_by_channel_no_filters(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            response = test_client.get('/incident/channels/percentage', headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert 'Llamada Telefónica' in data
            assert 'Correo Electronico' in data

    def test_get_percentage_of_incidents_by_channel_with_canal_filter(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
            
            response = test_client.get('/incident/channels/percentage', query_string={'canal_id': 1}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert 'Llamada Telefónica' in data
            assert sum(data.values()) == 30

    def test_get_percentage_of_incidents_by_channel_with_estado_filter(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            response = test_client.get('/incident/channels/percentage', query_string={'estado_id': 2}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert 'Correo Electronico' in data
            assert sum(data.values()) == 100
    
    def test_get_percentage_of_incidents_by_channel_with_date_range(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            db.session.query(Incidente).delete()
            db.session.commit()

            incidentes = [
                Incidente(
                    codigo=fake.uuid4(),
                    descripcion=fake.text(),
                    asunto=fake.sentence(),
                    fecha_creacion=datetime.now() - timedelta(days=2),
                    fecha_actualizacion=datetime.now() - timedelta(days=1),
                    canal_id=1,
                    usuario_creador_id=1,
                    usuario_asignado_id=2,
                    persona_id=1,
                    estado_id=1,
                    tipo_id=1
                ),
                Incidente(
                    codigo=fake.uuid4(),
                    descripcion=fake.text(),
                    asunto=fake.sentence(),
                    fecha_creacion=datetime.now() - timedelta(days=5),
                    fecha_actualizacion=datetime.now() - timedelta(days=4),
                    canal_id=2,
                    usuario_creador_id=1,
                    usuario_asignado_id=2,
                    persona_id=1,
                    estado_id=2,
                    tipo_id=2
                )
            ]
            db.session.bulk_save_objects(incidentes)
            db.session.commit()

            fecha_inicio = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
            fecha_fin = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            
            response = test_client.get('/incident/channels/percentage', query_string={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}, headers=headers)
            data = response.get_json()
            
            assert response.status_code == 200
            assert 'Correo Electrónico' in data
            assert sum(data.values()) == 100
    
    def test_get_percentage_of_incidents_by_channel_with_combined_filters(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            fecha_inicio = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
            
            response = test_client.get('/incident/channels/percentage', query_string={'canal_id': 1, 'estado_id': 1, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert 'Llamada Telefónica' in data
            assert sum(data.values()) == 100

    def test_get_percentage_of_incidents_by_channel_missing_authorization(self, mocker):
        with app.test_client() as test_client:
            response = test_client.get('/incident/channels/percentage')
            data = response.get_json()

            assert response.status_code == 500
            assert 'msg' in data
            assert data['msg'] == 'Error a la hora de conultar el detalle de la incidencia No se ha enviado el token, porfavor contacte con su administrador'

    def test_get_summary_incidents_no_filters(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            response = test_client.get('/incident/summary', headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 2
            assert all("id" in incident for incident in data['incidentes'])
    
    def test_get_summary_incidents_with_canal_filter(self, mocker):
       with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            response = test_client.get('/incident/summary', query_string={'canal_id': 1}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['canal'] == 'Llamada Telefónica'
    
    def test_get_summary_incidents_with_estado_filter(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            response = test_client.get('/incident/summary', query_string={'estado_id': 2}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['estado'] == 'Desestimado'

    def test_get_summary_incidents_with_date_range(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            fecha_inicio = (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d')
            fecha_fin = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            
            response = test_client.get('/incident/summary', query_string={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['canal'] == 'Correo Electrónico'
    
    def test_get_summary_incidents_with_combined_filters(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            fecha_inicio = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
            
            response = test_client.get('/incident/summary', query_string={'canal_id': 1, 'estado_id': 1, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}, headers=headers)
            data = response.get_json()

            assert response.status_code == 200
            assert data['total'] == 1
            assert data['incidentes'][0]['canal'] == 'Llamada Telefónica'
            assert data['incidentes'][0]['estado'] == 'Abierto'

    def test_get_summary_incidents_missing_authorization(self):
        with app.test_client() as test_client:
            response = test_client.get('/incident/summary')
            data = response.get_json()

            assert response.status_code == 500
            assert 'msg' in data
            assert 'Error a la hora de conultar el detalle de la incidencia' in data['msg']
