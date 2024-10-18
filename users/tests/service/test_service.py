import json
import pytest
from faker import Faker
from datetime import datetime
from src.main import app
from src.models.model import db, Product, ProductPerson
from src.service.service import UserService

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
