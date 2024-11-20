from faker import Faker
from src.main import app
from datetime import datetime
from google.auth.credentials import AnonymousCredentials 
import pytest

fake = Faker()       
        
class TestBlueprints():
    
    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client  
            
    def test_generacion_factura_incidencia(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
        
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})

        response_service = test_client.post('/invoice/create/5/1/es', headers=headers)
        invoice_data = response_service.get_json()
        
        print(invoice_data)

        assert response_service.status_code == 201
        
    def test_generacion_factura_pdf_incidencia(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        response_service = test_client.post('/invoice/create/5/1/es', headers=headers)
        invoice_data = response_service.get_json()
        
        print(invoice_data)
        
        response_service = test_client.get(f"/invoice/get-invoice-pdf/{invoice_data['id']}/es", headers=headers)

        assert response_service.status_code == 200    

    def test_envio_factura_pdf_correo(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        response_service = test_client.post('/invoice/create/5/1/es', headers=headers)
        invoice_data = response_service.get_json()
        
        print(invoice_data)
        
        mocker.patch('src.utils.utils.SendGridAPIClient.send', return_value=mocker.Mock(status_code=200, json=lambda: {'msg': "exito", "status_code": 201}))
 
        request = {
            "email": "test@gmail.com",
            "invoice_id": invoice_data['id'],
            "lang": "es"
        }
        
        response_service = test_client.post(f"/invoice/send-email", json=request, headers=headers)
        print(response_service.text)
        assert response_service.status_code == 201
        
    
    def test_encolar_pago(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)
        
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials, service_account_email='test_account@test.com'), 'project-id'))

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        response_service = test_client.post('/invoice/create/5/1/es', headers=headers)
        invoice_data = response_service.get_json()
        
        print(invoice_data)
        
        request = {
            "payment_method_id": 2,
            "id_invoice": invoice_data['id'],
        }
        
        mocker.patch('src.service.service.pubsub_v1.PublisherClient')
        
        response_service = test_client.post("/invoice/pay", json=request, headers=headers)
        print(response_service.text)
        assert response_service.status_code == 201
        
    def test_actualizar_factura(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)
        
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials, service_account_email='test_account@test.com'), 'project-id'))

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        headers = {'Authorization': "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3", "Technology": "WEB"}
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        response_service = test_client.post('/invoice/create/5/1/es', headers=headers)
        invoice_data = response_service.get_json()
        
        print(invoice_data)
        
        mocker.patch('src.service.service.pubsub_v1.PublisherClient')
        
        response_service = test_client.patch(f"/invoice/update/{invoice_data['id']}/Pagado", headers=headers)
        print(response_service.text)
        assert response_service.status_code == 201