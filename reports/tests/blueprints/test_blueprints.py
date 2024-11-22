import json
import pytest
from faker import Faker
from pytest_mock import MockerFixture, mocker
from requests import patch
from src.main import app
from src.models.model import db
from datetime import datetime, timedelta
from io import BytesIO
from src.service.report_service import ReportService

fake = Faker()       

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestBlueprints():
    def test_save_report_success(self, mocker: MockerFixture):
        with app.test_client() as test_client:
            mocker.patch('src.service.report_service.ReportService.fetch_incidents', return_value={
                "incidentes": [
                    {
                        "asunto": "incidente_llamada",
                        "canal": "Llamada Telefónica",
                        "codigo": "INC01565",
                        "estado": "Abierto",
                        "fecha_actualizacion": "11/15/2024",
                        "fecha_creacion": "11/15/2024",
                        "id": 5,
                        "tipo": "Petición"
                    },
                    {
                        "asunto": "internet",
                        "canal": "Correo Electrónico",
                        "codigo": "INC01235",
                        "estado": "Abierto",
                        "fecha_actualizacion": "11/15/2024",
                        "fecha_creacion": "11/15/2024",
                        "id": 7,
                        "tipo": "Queja/Reclamo"
                    },
                ],
                "total": 8
            })
            mocker.patch('src.service.report_service.ReportService.save_report', return_value=None)
            mocker.patch('src.service.report_service.ReportService.generate_pdf_report', return_value=BytesIO(b'mock_pdf_content'))
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
        
            response = test_client.post('/report/generate', headers=headers, json={
                    'canal_id': 1,
                    'estado_id': 2,
                    'fecha_inicio': '01/01/2024',
                    'fecha_fin': '01/31/2024',
                    'nombre_reporte': 'Reporte Test',
                    'tipo_id': 3
                }
            )

            assert response.status_code == 200
            assert response.content_type == 'application/pdf'

    def test_save_report_missing_data(self, mocker: MockerFixture):
        with app.test_client() as test_client:

            mocker.patch('src.service.report_service.ReportService.fetch_incidents', return_value={
                "incidentes": [
                    {
                        "asunto": "incidente_llamada",
                        "canal": "Llamada Telefónica",
                        "codigo": "INC01565",
                        "estado": "Abierto",
                        "fecha_actualizacion": "11/15/2024",
                        "fecha_creacion": "11/15/2024",
                        "id": 5,
                        "tipo": "Petición"
                    },
                    {
                        "asunto": "internet",
                        "canal": "Correo Electrónico",
                        "codigo": "INC01235",
                        "estado": "Abierto",
                        "fecha_actualizacion": "11/15/2024",
                        "fecha_creacion": "11/15/2024",
                        "id": 7,
                        "tipo": "Queja/Reclamo"
                    },
                ],
                "total": 8
            })
            mocker.patch('src.service.report_service.ReportService.save_report', return_value=None)
            mocker.patch('src.service.report_service.ReportService.generate_pdf_report', return_value=BytesIO(b'mock_pdf_content'))
            mocker.patch('src.validations.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))

            headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}

            response = test_client.post('/report/generate', headers=headers, json={} )

            assert response.status_code == 500
            assert b'{"msg":"Error en el sistema porfavor contacte con el administrador"}\n' in response.data
        
    def test_health_check(client):
        with app.test_client() as test_client:
            response = test_client.get('/report/ping')
            assert response.status_code == 200
            assert response.data == b'pong'

    def test_send_email_success(self, mocker: MockerFixture):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.ValidatorReports.validate_token_sent', return_value=None)
            mocker.patch('src.validations.validations.ValidatorReports.valid_token', return_value=None)
            mocker.patch('src.service.report_service.ReportService.fetch_incidents', return_value={
                "incidentes": [
                    {
                        "asunto": "Prueba incidente",
                        "canal": "Email",
                        "codigo": "INC1234",
                        "estado": "Abierto",
                        "fecha_actualizacion": "11/15/2024",
                        "fecha_creacion": "11/14/2024",
                        "id": 1,
                        "tipo": "Petición"
                    }
                ],
                "total": 1
            })
            mocker.patch('src.service.report_service.ReportService.save_report', return_value=None)
            mocker.patch('src.service.report_service.ReportService.generate_pdf_report', return_value=BytesIO(b'PDF content'))
            mocker.patch('src.service.report_service.ReportService.send_report_pdf_by_email', return_value={'status': 'success'})

            headers = {'Authorization': "Bearer valid-token", "Technology": "WEB"}
            payload = {
                'canal_id': 1,
                'estado_id': 2,
                'fecha_inicio': '01/01/2024',
                'fecha_fin': '01/31/2024',
                'nombre_reporte': 'Reporte Test',
                'tipo_id': 3,
                'lang': 'es',
                'email': 'test@example.com'
            }

            response = test_client.post('/report/sendemail', headers=headers, json=payload)

            assert response.status_code == 200
            assert response.content_type == 'application/pdf'   

    def test_send_email_missing_data(self, mocker: MockerFixture):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.ValidatorReports.validate_token_sent', return_value=None)
            mocker.patch('src.validations.validations.ValidatorReports.valid_token', return_value=None)

            headers = {'Authorization': "Bearer valid-token", "Technology": "WEB"}
            response = test_client.post('/report/sendemail', headers=headers, json={})

            assert response.status_code == 500
            assert b"Error en el sistema porfavor contacte con el administrador" in response.data        

    def test_send_email_invalid_token(self, mocker: MockerFixture):
        with app.test_client() as test_client:
            mocker.patch('src.validations.validations.ValidatorReports.validate_token_sent', side_effect=Exception("Token inválido"))

            headers = {'Authorization': "Bearer invalid-token", "Technology": "WEB"}
            payload = {
                'canal_id': 1,
                'estado_id': 2,
                'fecha_inicio': '01/01/2024',
                'fecha_fin': '01/31/2024',
                'nombre_reporte': 'Reporte Test',
                'tipo_id': 3,
                'lang': 'es',
                'email': 'test@example.com'
            }

            response = test_client.post('/report/sendemail', headers=headers, json=payload)

            assert response.status_code == 500
            assert b"Error en el sistema porfavor contacte con el administrador" in response.data       

