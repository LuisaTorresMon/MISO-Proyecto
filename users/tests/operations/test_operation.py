import json
import pytest
from faker import Faker
from src.main import app

fake = Faker()    

class TestOperations():

    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client
            
    def test_create_person(self):   
        with app.test_client() as test_client:
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}

            person_data = {
                'name': fake.first_name(),
                'lastname': fake.last_name(),
                'email': fake.email(),
                'identity_type': fake.random_element(elements=('Cedula_ciudadania', 'Cedula_extranjeria', 'Pasaporte')),
                'identity_number': fake.random_number(digits=10),
                'cellphone': fake.phone_number()
            }

            response_service = test_client.post('/user/person/create',json=person_data, headers=headers)
            
            assert response_service.status_code == 201


