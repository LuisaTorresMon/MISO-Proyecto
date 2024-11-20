import pytest
from src.main import app
from src.service.service import InvoiceService
from datetime import datetime
from google.auth.credentials import AnonymousCredentials 

invoice_service = InvoiceService()

class TestService():
    
    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client
            
    def test_get_active_plan_by_company(self, mocker):
        with app.test_client() as test_client:
           
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            mocker.patch('src.service.service.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
 
            invoice_service.get_active_plan_by_company(token, 1)
            
    def test_get_incidents_count_by_username(self, mocker):
        with app.test_client() as test_client:
           
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            mocker.patch('src.service.service.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
 
            invoice_service.get_incidents_count_by_username(token, 1, 2)
            
    def test_get_company(self, mocker):
        with app.test_client() as test_client:
           
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"
            mocker.patch('src.service.service.requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
 
            invoice_service.get_company(token, 1)
            
    def test_generacion_factura_incidencia(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)
        
        token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})

        invoice = invoice_service.build_invoice_client(token, 5, 1, 'es')
        
        assert invoice
        
    def test_generacion_factura_pdf_incidencia(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)
        
        token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})

        invoice = invoice_service.build_invoice_client(token, 5, 1, 'es')
        pdf_response = invoice_service.get_invoice_pdf(token, invoice['id'], 'en')
        
        assert pdf_response
        
    def test_envio_factura_pdf_correo(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)
        
        token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3"

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        
        mocker.patch('src.utils.utils.SendGridAPIClient.send', return_value=mocker.Mock(status_code=200, json=lambda: {'msg': "exito", "status_code": 201}))
 
        invoice = invoice_service.build_invoice_client(token, 5, 1, 'es')
        email_response = invoice_service.send_invoice_pdf_by_email(token,'test@test.com', invoice['id'], 'en')
 
        assert email_response
        
    
    def test_encolar_pago(self, mocker):
      with app.test_client() as test_client:

        current_year = datetime.now().year
        first_day_year = datetime(current_year, 1, 1)
        
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials, service_account_email='test_account@test.com'), 'project-id'))

        mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
        mocker.patch('src.service.service.InvoiceService.get_active_plan_by_company', return_value={'fecha_inicio_plan': f"{first_day_year}", 'precio_plan': 500})
        mocker.patch('src.service.service.InvoiceService.get_incidents_count_by_username', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.InvoiceService.get_company', return_value={'total_price': 1, 'incident_count': 1, 'channel_price': 1})
        mocker.patch('src.service.service.pubsub_v1.PublisherClient')

        invoice_service.pay_menthod_queue(1, 2)
        
        