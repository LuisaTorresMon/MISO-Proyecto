import json
import pytest
from faker import Faker
from datetime import datetime
from src.main import app
from src.models.model import db, Product, ProductPerson
from src.errors.errors import TokenNoEnviado, TokenVencido, BadRequestException, EmailInvalido, TelefonoNoNumerico, PassNoCoincide, PassNoValido
from src.validators.validator import UserValidator
from flask_jwt_extended import jwt_required, create_access_token, get_current_user, get_jwt

fake = Faker()
headers = {"Authorization": "Bearer 123456"}

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_ok_authorization(mocker):
    mock = mocker.patch('requests.get')
    mock.return_value.status_code = 200
    return mock

@pytest.fixture
def mock_create_user(mocker):
    return mocker.patch('src.service.service.UserService.create_user')

@pytest.fixture
def mock_empresa(mocker):
    return mocker.patch('src.models.model.Empresa')

@pytest.fixture
def mock_persona(mocker):
    return mocker.patch('src.models.model.Person')

@pytest.fixture
def mock_validate(mocker):
    return mocker.patch('src.validator.validator.validate_registration_data')

class TestOperations():

    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client
            
    def test_create_person(self):   
        with app.test_client() as test_client:
          
            token = self.generate_token()

            headers = {'Authorization': f"Bearer {token}"}

            response_service = self.create_person(headers)
            print(response_service.text)
            print(response_service.get_json())
            
            assert response_service.status_code == 201 
            
    def test_find_person_by_identity(self):   
        with app.test_client() as test_client:
          
            token = self.generate_token()

            headers = {'Authorization': f"Bearer {token}"}

            person_response = self.create_person(headers)
            print(person_response.text)
            print(person_response.get_json())
               
            person_data = person_response.get_json()
            response_query = test_client.get(f"/user/person?identityType={person_data.get('tipo_identificacion')}&identityNumber={person_data.get('numero_identificacion')}",json=person_data, headers=headers)
            data_query = response_query.get_json()
            
            assert response_query.status_code == 200
            assert data_query.get('tipo_identificacion') == person_data.get('tipo_identificacion') and data_query.get('numero_identificacion') == person_data.get('numero_identificacion')

    def test_find_person_by_id(self):   
        with app.test_client() as test_client:
          
            token = self.generate_token()

            headers = {'Authorization': f"Bearer {token}"}

            person_response = self.create_person(headers)
            print(person_response.text)
            print(person_response.get_json())
               
            person_data = person_response.get_json()
            response_query = test_client.get(f"/user/person/{person_data['id']}",json=person_data, headers=headers)
            data_query = response_query.get_json()
            
            assert response_query.status_code == 200
            assert data_query.get('tipo_identificacion') == person_data.get('tipo_identificacion') and data_query.get('numero_identificacion') == person_data.get('numero_identificacion')

    def test_find_user_by_id(self):   
        with app.test_client() as test_client:
          
            token = self.generate_token()
            
            headers = {'Authorization': f"Bearer {token}"}

            user_data = {
                'id_person': '4',
                'id_company': None,
                'id_typeuser': '1',
                'username': fake.user_name(),
                'password': 'password123'
            }

            user = test_client.post('/user/create', json=user_data)
            user_data = user.get_json()
            
            response_query = test_client.get(f"/user/get/{user_data['id']}", headers=headers)
            data_query = response_query.get_json()
            
            assert response_query.status_code == 200
            

    def test_find_product_by_person(self):   
        with app.test_client() as test_client:
          
            token = self.generate_token()

            headers = {'Authorization': f"Bearer {token}"}

            person_response = self.create_person(headers)
            print(person_response.text)
            print(person_response.get_json())
            person_data = person_response.get_json()

            
            product = self.create_product()
            self.create_product_person(product.id, person_data.get('id'))
               
            response_query = test_client.get(f"/user/person/{person_data.get('id')}/products",headers=headers)
            
            assert response_query.status_code == 200

    def test_update_person(self):   
        with app.test_client() as test_client:
          
            token = self.generate_token()

            headers = {'Authorization': f"Bearer {token}"}

            person_response = self.create_person(headers)
            print(person_response.text)
            print(person_response.get_json())
               
            person_data = person_response.get_json()
            
            person_new_data = {
                'identity_type': person_data.get('tipo_identificacion'),
                'identity_number': person_data.get('numero_identificacion'),
                'name': fake.first_name(),
                'lastname': fake.last_name(),
                'email': fake.email(),
                'cellphone': fake.phone_number()
            }
            
            print(person_new_data)  
            response_update = test_client.put("/user/person/update",json=person_new_data, headers=headers)
            
            assert response_update.status_code == 200
            
    def create_product(self):
        with app.test_client() as test_client:

            new_product = Product(
            nombre_producto=fake.word(),
            tipo=fake.word(),
            descripcion=fake.sentence()
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return new_product
        
    def create_product_person(self, id_producto, id_persona):
        with app.test_client() as test_client:

            new_product_person = ProductPerson(
                fecha_adquisicion=datetime.now(),
                id_persona=id_persona,
                id_producto=id_producto
            )
        
        db.session.add(new_product_person)
        db.session.commit()
    
    def create_person(self, headers):
        with app.test_client() as test_client:

            person_data = {
                'name': fake.first_name(),
                'lastname': fake.last_name(),
                'email': fake.email(),
                'identity_type': fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                'identity_number': fake.random_number(digits=10),
                'cellphone': fake.phone_number()
            }

            response = test_client.post('/user/person/create',json=person_data, headers=headers)
            
            return response

    def generate_token(self):
        with app.test_client() as test_client:
          
            login_data = {
                "username": "sa",
                "password": "123456",
                "technology": "WEB"
            }
                        
            response_jwt = test_client.post('/user/auth/login',json=login_data)
            data_jwt = response_jwt.get_json()
            
            return data_jwt.get('token')     
        
    def test_health(self):
        with app.test_client() as test_client:
            response = test_client.get('/user/ping')

            assert response.status_code == 200
            assert response.data == b'pong'

    def test_register_client(self, client, mock_create_user, mock_empresa):
        with app.test_client() as test_client:

            password = fake.password()

            user_data = {
                "nombre_empresa": fake.company(),
                "email": fake.email(),
                "tipo_identificacion": fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                "numero_identificacion": fake.random_number(digits=10),
                "sector": fake.company(),
                "telefono": fake.random_number(digits=10),
                "pais": fake.country(),
                "usuario": fake.user_name(),
                "contrasena": password,
                "confirmar_contrasena": password
            }

            mock_create_user.return_value = {
                "nombre_usuario": user_data['usuario']
            }

            mock_empresa.return_value.id = 1

            response = client.post(
                '/user/register/client',  
                data=json.dumps(user_data),
                content_type='application/json'
            )

            assert response.status_code == 200

    def test_validate_registration_data_missing_email(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()

            user_type = 'client'

            user_data = {
                "nombre_empresa": fake.company(),
                "email": None,
                "tipo_identificacion": fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                "numero_identificacion": fake.random_number(digits=10),
                "sector": fake.company(),
                "telefono": fake.random_number(digits=10),
                "pais": fake.country(),
                "usuario": fake.user_name(),
                "contrasena": password,
                "confirmar_contrasena": password
            }

            mock_create_user.return_value = {
                "nombre_usuario": user_data['usuario']
            }

            with pytest.raises(BadRequestException, match="El campo email es obligatorio."):
                UserValidator.validate_registration_data(user_data, user_type)

    def test_validate_registration_data_missing_telefone(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()
            user_type = 'client'

            user_data = {
                "nombre_empresa": fake.company(),
                "email": fake.email(),
                "tipo_identificacion": fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                "numero_identificacion": fake.random_number(digits=10),
                "sector": fake.company(),
                "telefono": "Prueba",
                "pais": fake.country(),
                "usuario": fake.user_name(),
                "contrasena": password,
                "confirmar_contrasena": password
            }

            mock_create_user.return_value = {
                "nombre_usuario": user_data['usuario']
            }

            with pytest.raises(TelefonoNoNumerico, match="El campo de teléfono debe contener solo números"):
                UserValidator.validate_registration_data(user_data, user_type)

    def test_validate_registration_data_missing_password(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()
            user_type = 'client'

            user_data = {
                "nombre_empresa": fake.company(),
                "email": fake.email(),
                "tipo_identificacion": fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                "numero_identificacion": fake.random_number(digits=10),
                "sector": fake.company(),
                "telefono": fake.random_number(digits=10),
                "pais": fake.country(),
                "usuario": fake.user_name(),
                "contrasena": password,
                "confirmar_contrasena": fake.user_name()
            }

            mock_create_user.return_value = {
                "nombre_usuario": user_data['usuario']
            }

            with pytest.raises(PassNoCoincide, match="Las contraseñas no coinciden"):
                UserValidator.validate_registration_data(user_data, user_type)
    
    def test_validate_registration_data_missing_field(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()
            user_type = 'client'

            user_data = {
                "nombre_empresa": fake.company(),
                "email": fake.email(),
                "tipo_identificacion": fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                "numero_identificacion": fake.random_number(digits=10),
                "sector": fake.company(),
                "telefono": fake.random_number(digits=10),
                "pais": fake.country(),
                "contrasena": password,
                "confirmar_contrasena": password,
                "usuario": ""
            }

            mock_create_user.return_value = {
                "nombre_usuario": user_data['usuario']
            }

            with pytest.raises(BadRequestException, match="El campo usuario es obligatorio."):
                UserValidator.validate_registration_data(user_data, user_type)

    def test_is_valid_password(self):
        password = fake.password()

        result = UserValidator.is_valid_password(password)
        print(f"el resultado {result}")
        assert result == True

    def test_register_agent(self, client, mock_create_user, mock_persona):
        with app.test_client() as test_client:

            token = self.generate_token()

            headers = {'Authorization': f"Bearer {token}"}

            password = fake.password()

            user_data = {
                "nombres": fake.company(),
                "apellidos": fake.company(),
                "correo_electronico": fake.email(),
                "tipo_identificacion": fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                "numero_identificacion": fake.random_number(digits=10),
                "telefono": fake.random_number(digits=10),
                "usuario": fake.user_name(),
                "contrasena": password,
                "confirmar_contrasena": password
            }

            mock_create_user.return_value = {
                "nombre_usuario": user_data['usuario']
            }

            mock_persona.return_value.id = 1

            print(user_data)

            response = client.post(
                '/user/register/agent',  
                data=json.dumps(user_data),
                content_type='application/json',
                headers=headers
            )

            assert response.status_code == 200

    def test_create_user(self, client):
        user_data = {
            'id_person': '4',
            'id_company': None,
            'id_typeuser': '1',
            'username': fake.user_name(),
            'password': 'password123'
        }

        response = client.post('/user/create', json=user_data)

        assert response.status_code == 201

    def test_validate_token_success(self, client, mocker):
        access_token = create_access_token(identity='test_user')

        mocker.patch('flask_jwt_extended.get_jwt', return_value={'sub': 'test_user'})

        response = client.post('/user/auth/validate-token', headers={'Authorization': f'Bearer {access_token}'})

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['sub'] == 'test_user'

    def test_validate_token_without_jwt(self, client):
        response = client.post('/user/auth/validate-token')

        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert 'msg' in response_data