import json
from src.main import app
import pytest
from faker import Faker

fake = Faker()
headers = {"Authorization": "Bearer 123456"}
SIZES = ["LARGE", "MEDIUM", "SMALL"]

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_ok_authorization(mocker):
    mock = mocker.patch('requests.get')
    mock.return_value.status_code = 200
    return mock

class TestOffers():

    def test_health(self):
        with app.test_client() as test_client:
            response = test_client.get('/offers/ping')

            assert response.status_code == 200
            assert response.data == b'pong'
        
    def test_creacion_oferta(self, mocker, client):
        with app.test_client() as test_client:
            
            mocker.patch('src.commands.create.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            mocker.patch('src.utils.utils.FileUtils.get_user', return_value='1234567890')
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
            data = self.request_offer_data()
            response_service = test_client.post('/offers',json=data, headers=headers)
            
            assert response_service.status_code == 201

    def test_creacion_fallida(self, mock_ok_authorization):
        with app.test_client() as test_client:
            headers = {"Authorization": "Bearer 123456"}
            response = test_client.post('/offers', json={
                "postId": fake.name(),
                "description": fake.sentence(),
                "size": fake.random_element(SIZES),
                "fragile": fake.pybool(),
                "offer": -1
            }, headers=headers)

            assert response.status_code == 412

    def test_sin_campos(self, mock_ok_authorization):
        with app.test_client() as test_client:
            response = test_client.post('/offers', json={}, headers=headers)

            assert response.status_code == 400

    def test_sin_token(self):
        with app.test_client() as test_client:
            response = test_client.post('/offers', json={})

            assert response.status_code == 403

    def test_listar_offer_sin_filtros(self, mocker, client):
        with app.test_client() as test_client:
            mocker.patch('src.commands.list.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'ofertas': [{'id': '1', 'createdAt': '2024-02-07T03:12:05.098636', 'description': 'Oferta 1'}, {'id': '2', 'createdAt': '2024-02-07T03:12:05.098636', 'description': 'Oferta 2'}]}))
            mocker.patch('src.utils.utils.FileUtils.get_user', return_value='1234567890')
            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"}
            
            offers = test_client.get('/offers', headers=headers)
            offers_data = json.loads(offers.data)

            assert offers.status_code == 200
            assert offers is not None

    def test_listar_owner(self, mock_ok_authorization):
        with app.test_client() as test_client:
            response = test_client.get('/offers?owner=abc', headers=headers)

            assert response.status_code == 200
    
    def test_token_noenviado_listar_owner(self):
        with app.test_client() as test_client:
            response = test_client.get('/offers?owner=abc')

            assert response.status_code == 403

    def test_listar_id_fallida(self, mock_ok_authorization):
        with app.test_client() as test_client:
            response = test_client.get('/offers/abc', headers=headers)

            assert response.status_code == 400

    def test_token_noenviado_listar_id(self):
        with app.test_client() as test_client:
            response = test_client.get('/offers/abc')

            assert response.status_code == 403

    def test_delete_fallido(self, mock_ok_authorization):
        with app.test_client() as test_client:
            response = test_client.delete('/offers/abc', headers=headers)

            assert response.status_code == 400

    def test_token_noenviado_delete(self):
        with app.test_client() as test_client:
            response = test_client.delete('/offers/abc')

            assert response.status_code == 403
    
    def request_offer_data(self):
        data = {
            'postId': fake.random_int(),
            'userId': fake.random_int(),
            'description': fake.sentence(),
            'size': fake.random_element(SIZES),
            'fragile': fake.boolean(),
            'offer': fake.random_int(min=0)
        }
        
        return data
    