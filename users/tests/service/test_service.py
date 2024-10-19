import bcrypt
import pytest
import json
from faker import Faker
from datetime import datetime
from src.main import app
from src.models.model import db, Product, ProductPerson
from src.service.service import UserService
from src.errors.errors import IncorrectUserOrPasswordException, UserAlreadyExistException, BadRequestException

fake = Faker()    
user_service = UserService()

class TestServices():
    
    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client
            
    def test_create_person(self):   
        with app.test_client() as test_client:
            new_person = self.create_person()
            assert new_person['id'] is not None
            
    def test_find_product_by_person(self):  
        with app.test_client() as test_client:
            new_person = self.create_person()
            
            identity_type = new_person['tipo_identificacion']
            identity_number = new_person['numero_identificacion']
            
            person_query = user_service.get_person_by_identity(identity_type, identity_number)
            
            assert new_person['id'] == person_query.id
 
    def test_update_person(self):   
        with app.test_client() as test_client:
            new_person = self.create_person()
            
            identity_type = new_person['tipo_identificacion']
            identity_number = new_person['numero_identificacion']
            
            person_new_data = {
                'identity_type': identity_type,
                'identity_number': identity_number,
                'name': fake.first_name(),
                'lastname': fake.last_name(),
                'email': fake.email(),
                'cellphone': fake.phone_number()
            }
            
            updated_person = user_service.update_person(person_new_data)
            
            assert new_person['id'] == updated_person['id']
            
    def test_find_person_product(self):   
        new_person = self.create_person()

        product = self.create_product()
        self.create_product_person(product.id, new_person['id'])

        products_schema = user_service.get_products_by_person(new_person['id'])
        
        assert len(products_schema) > 0

    def test_create_user_success(self, mocker):

        mock_data = {
            'id_person': '1',
            'id_company': None,
            'id_typeuser': '2',
            'username': 'testuser',
            'password': 'password123'
        }


        mocker.patch('src.models.model.User.query.filter_by', return_value=None)


        mocker.patch('src.models.model.db.session.commit')


        mocker.patch('bcrypt.gensalt', return_value=b'salt')
        mocker.patch('bcrypt.hashpw', return_value=b'hashed_password')

        result = user_service.create_user(mock_data)

        assert result['nombre_usuario'] == 'testuser'

    def test_create_user_invalid_id_person_raises_exception(self, mocker):
        # Datos simulados con un `id_person` no convertible a entero
        mock_data = {
            'id_person': 'invalid',
            'id_company': None,
            'id_typeuser': '2',
            'username': 'testuser',
            'password': 'password123'
        }

        # Verificar que lanza BadRequestException al no poder convertir id_persona a entero
        with pytest.raises(BadRequestException):
            user_service.create_user(mock_data)

    def test_create_user_invalid_id_empresa_raises_exception(self, mocker):
        # Datos simulados con un `id_empresa` no convertible a entero
        mock_data = {
            'id_person': None,
            'id_company': 'invalid_company',
            'id_typeuser': '2',
            'username': 'testuser',
            'password': 'password123'
        }

        # Verificar que lanza BadRequestException al no poder convertir id_empresa a entero
        with pytest.raises(BadRequestException):
            user_service.create_user(mock_data)

    def test_create_user_already_exists_raises_exception(self, mocker):

        mock_data = {
            'id_person': '1',
            'id_company': None,
            'id_typeuser': '2',
            'username': 'testuser',
            'password': 'password123'
        }

        mocker.patch('src.models.model.User.query.filter_by', return_value=True)

        with pytest.raises(UserAlreadyExistException):
            user_service.create_user(mock_data)

    def test_create_user_missing_params_raises_exception(self):
        mock_data = {
            'id_person': None,
            'id_company': None,
            'id_typeuser': None,
            'username': 'testuser',
            'password': 'password123'
        }

        with pytest.raises(BadRequestException):
            user_service.create_user(mock_data)

    def test_create_user_invalid_id_typeuser_raises_exception(self):
        mock_data = {
            'id_person': None,
            'id_company': '2',
            'id_typeuser': 'invalid',
            'username': 'testuser',
            'password': 'password123'
        }


        with pytest.raises(BadRequestException):
            user_service.create_user(mock_data)

    def test_create_user_valid_id_person_id_company_raises_exception(self):
        mock_data = {
            'id_person': '4',
            'id_company': '2',
            'id_typeuser': '1',
            'username': 'testuser',
            'password': 'password123'
        }

        with pytest.raises(BadRequestException):
                    user_service.create_user(mock_data)

    def test_create_user_bad_credentials_by_username_raises_exception(self, mocker):
        mock_user = {
            'username': 'invalid_username',
            'password': 'password123'
        }
        mocker.patch('src.models.model.User.query.filter_by', return_value=mocker.Mock(first=lambda: None))

        mock_user_query = mocker.MagicMock()
        mock_user_query.first.return_value = None
        mocker.patch('src.models.model.User.query.filter_by', return_value=mock_user_query)

        with pytest.raises(IncorrectUserOrPasswordException ):
            user_service.signIn(mock_user)

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

    def create_person(self):
        with app.test_client() as test_client:

            person_data = {
                'name': fake.first_name(),
                'lastname': fake.last_name(),
                'email': fake.email(),
                'identity_type': fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                'identity_number': fake.random_number(digits=10),
                'cellphone': fake.phone_number()
            }

            new_person = user_service.create_person(person_data)
            return new_person

    def create_user(self):
        with app.test_client() as test_client:
            user_data = {
                'id_person': '4',
                'id_company': None,
                'id_typeuser': '1',
                'username': 'testuser',
                'password': self.generate_credentials('password123')
            }

        new_user = user_service.create_user(user_data)
        return new_user

    def generate_credentials(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        return hashed_password.decode('utf-8')