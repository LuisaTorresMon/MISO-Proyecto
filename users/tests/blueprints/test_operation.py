import json
import pytest
from faker import Faker
from datetime import datetime
from src.main import app
from src.models.model import db, Product, ProductPerson

fake = Faker()    

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
                "password": "123456"
            }
                        
            response_jwt = test_client.post('/user/auth/login',json=login_data)
            data_jwt = response_jwt.get_json()
            
            return data_jwt.get('token')       
