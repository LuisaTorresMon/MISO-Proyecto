import json
from unittest.mock import patch
from src.main import app
import pytest
from faker import Faker
from src.errors.errors import TokenNoEnviado, TokenVencido, BadRequestException, EmailInvalido, TelefonoNoNumerico, PassNoCoincide, PassNoValido
from src.validators.validator import UserValidator

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
def mock_validate(mocker):
    return mocker.patch('src.validator.validator.validate_registration_data')

class TestUsers():
    def test_health(self):
        with app.test_client() as test_client:
            response = test_client.get('/user/ping')

            assert response.status_code == 200
            assert response.data == b'pong'

    def test_register_client(self, client, mock_create_user, mock_empresa):
        with app.test_client() as test_client:

            password = fake.password()

            user_data = {
                "nombre_completo": fake.company(),
                "email": fake.email(),
                "tipo_documento": fake.random_number(digits=1),
                "numero_documento": fake.random_number(digits=10),
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

            user_data = {
                "nombre_completo": fake.company(),
                "email": None,
                "tipo_documento": fake.random_number(digits=1),
                "numero_documento": fake.random_number(digits=10),
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

            with pytest.raises(EmailInvalido, match="El formato del email no es válido"):
                UserValidator.validate_registration_data(user_data)

    def test_validate_registration_data_missing_telefone(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()

            user_data = {
                "nombre_completo": fake.company(),
                "email": fake.email(),
                "tipo_documento": fake.random_number(digits=1),
                "numero_documento": fake.random_number(digits=10),
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
                UserValidator.validate_registration_data(user_data)

    def test_validate_registration_data_missing_password(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()

            user_data = {
                "nombre_completo": fake.company(),
                "email": fake.email(),
                "tipo_documento": fake.random_number(digits=1),
                "numero_documento": fake.random_number(digits=10),
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
                UserValidator.validate_registration_data(user_data)
    
    def test_validate_registration_data_missing_field(self, mock_create_user):
        with app.test_client() as test_client:

            password = fake.password()

            user_data = {
                "nombre_completo": fake.company(),
                "email": fake.email(),
                "tipo_documento": fake.random_number(digits=1),
                "numero_documento": fake.random_number(digits=10),
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
                UserValidator.validate_registration_data(user_data)

    def test_is_valid_password(self):
        password = fake.password()

        result = UserValidator.is_valid_password(password)
        print(f"el resultado {result}")
        assert result == True
