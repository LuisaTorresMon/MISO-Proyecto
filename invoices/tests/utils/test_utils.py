import pytest
from src.main import app
from datetime import datetime
from src.utils.utils import CommonUtils

common_utils = CommonUtils()

class TestUtils():
    
    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client
            
            
    def test_envio_correo(self, mocker):
      with app.test_client() as test_client:
                
        mocker.patch('src.utils.utils.SendGridAPIClient.send', return_value=mocker.Mock(status_code=200, json=lambda: {'msg': "exito", "status_code": 201}))
        common_utils.send_email('test@test.com', 'test', 'test')
        
    def test_generate_token(self, mocker):
      with app.test_client() as test_client:
          
        token = 'Bearer test'
                
        mocker.patch('src.utils.utils.SendGridAPIClient.send', return_value=mocker.Mock(status_code=200, json=lambda: {'msg': "exito", "status_code": 201}))
        common_utils.obtener_token(token)
    