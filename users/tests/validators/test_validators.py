import pytest
from src.main import app
from src.errors.errors import TokenNoEnviado, RequiredFields, TokenVencido, BadRequestException, EmailInvalido, TelefonoNoNumerico, PassNoCoincide, PassNoValido
from src.validators.validator import UserValidator

user_validator = UserValidator()

class TestValidators():
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    def test_validar_request_creacion_success(self):
        headers = {'Authorization': 'Bearer token'}
        data = {'username': 'test_user', 'password': 'ValidPassword1'}
        result = user_validator.validar_request_creacion(headers, data)
        assert result is True

    def test_validar_request_creacion_token_no_enviado(self):
        headers = {}
        data = {'username': 'test_user', 'password': 'ValidPassword1'}
        with pytest.raises(TokenNoEnviado):
            user_validator.validar_request_creacion(headers, data)

    def test_validar_request_creacion_token_vencido(self):
        headers = {'Authorization': 'Bearer fake.expired_token'}
        data = {'username': 'test_user', 'password': 'ValidPassword1'}
        with pytest.raises(TokenVencido):
            user_validator.validar_request_creacion(headers, data)

    def test_validate_query_person_success(self):
        user_validator.validate_query_person('ID', '12345678')

    def test_validate_query_person_missing_fields(self):
        with pytest.raises(RequiredFields):
            user_validator.validate_query_person('', '')

    def test_validar_listado_success(self):
        headers = {'Authorization': 'Bearer token'}
        result = user_validator.validar_listado(headers)
        assert result is True

    def test_validar_consulta_success(self):
        headers = {'Authorization': 'Bearer token'}
        result = user_validator.validar_consulta(headers)
        assert result is True