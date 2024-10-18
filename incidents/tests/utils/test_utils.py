import pytest
from io import BytesIO
from faker import Faker
from src.main import app
from src.utils.utils import CommonUtils
from google.auth.credentials import AnonymousCredentials 
import os

fake = Faker()       
common_utils = CommonUtils()

class FileWithContentType(BytesIO):
    def __init__(self, content, content_type):
        super().__init__(content)
        self.content_type = content_type

class TestUtils():
    
    @pytest.fixture 
    def client(self):
      with app.test_client() as client:
        yield client
        
    def test_subir_archivo_bucker(self, mocker):
        
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
        mocker.patch('google.cloud.storage.Client')
        
        file = BytesIO(b"archivo de prueba test_subir_archivo_bucker")
        file.content_type = 'text/plain'
        destination_blob_name = 'blob.txt'
        
        common_utils.upload_file_to_gcs_by_file(file, destination_blob_name) 
        
    def test_subir_archivo_ruta(self, mocker):
        
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
        mocker.patch('google.cloud.storage.Client')
 
        audio_path = os.path.join('audios', 'llamada_1.mp3')
        
        common_utils.upload_file_to_gcs_by_path(audio_path, 'blob.mp3')    
        
    
