import pytest
from faker import Faker
from src.main import app
from src.validations.validations import ValidatorIncidents
from src.errors.errors import RequiredFields, BadRequestError, InvalidToken, TokenEmpty

fake = Faker()       
validator = ValidatorIncidents()

class TestValidations():
    
    @pytest.fixture 
    def client(self):
      with app.test_client() as client:
        yield client    
        
      
    def test_campos_sin_nombre_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

            incident_type= fake.name()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
            
    def test_campos_sin_apellido_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            incident_type= fake.name()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
            
    def test_campos_sin_email_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            incident_type= fake.name()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
         
    def test_campos_sin_tipo_identificacion_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            incident_type= fake.name()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
         
    def test_campos_sin_numero_identificacion_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            incident_type= fake.name()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
        
    def test_campos_sin_celular_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            incident_type= fake.name()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
         
    def test_campos_sin_tipo_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

            incident_type= None
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            with pytest.raises(RequiredFields):
                validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
         
    def test_campos_sin_canal_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            
            incident_type= fake.word()
            incident_channel= None
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= fake.sentence(nb_words=8)
            
            with pytest.raises(RequiredFields):
                validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
    
    def test_campos_sin_titulo_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

            incident_type= fake.word()
            incident_channel= fake.word()
            incident_subject = None,
            incident_detail= fake.sentence(nb_words=8)
            
            with pytest.raises(RequiredFields):
                validator.validate_incident_data(incident_type, incident_channel, incident_subject, incident_detail, token) 
         
    def test_campos_sin_titulo_incidencia_creacion_incidencia(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

            incident_type= fake.word()
            incident_channel= fake.word()
            incident_subject = fake.sentence(nb_words=8),
            incident_detail= None
            
            with pytest.raises(RequiredFields):
                validator.validate_incident_data( incident_type, incident_channel, incident_subject, incident_detail, token) 
         
    def test_email_valido(self):
        with app.test_client() as test_client:
            validator.email_person = fake.name()
            
            with pytest.raises(BadRequestError):
                validator.validar_correo_electronico()  
                
    def test_celular_valido(self):
        with app.test_client() as test_client:
            validator.cellphone_person = fake.name()
            
            with pytest.raises(BadRequestError):
                validator.validar_celular() 
                
    def test_numero_documento_cedula_ciudadania_valido(self):
        with app.test_client() as test_client:
            validator.identity_type_person = 'Cédula_Cuidadania'
            validator.identity_number_person = fake.name()
            
            with pytest.raises(BadRequestError):
                validator.validar_numero_de_documento()  
                
    def test_numero_documento_cedula_extrangeria_valido(self):
        with app.test_client() as test_client:
            validator.identity_type_person = 'Cédula_Extrangeria'
            validator.identity_number_person = fake.name()
            
            with pytest.raises(BadRequestError):
                validator.validar_numero_de_documento()    
                
    def test_token_vacio(self):
        with app.test_client() as test_client:

            with pytest.raises(TokenEmpty):
                validator.validate_token_sent(None)          
 
    def test_token_invalido(self, mocker):
        with app.test_client() as test_client:

            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=401, json=lambda: {'respuesta': 'Token invalido'}))
            token = "Bearer fake"


            with pytest.raises(InvalidToken):
                validator.valid_token(token)          
