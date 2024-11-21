import pytest
from src.main import app
from src.service.service import PaymentService

payment_service = PaymentService()

class TestService():
    
    @pytest.fixture 
    def client(self):
      with app.test_client() as client:
        yield client
        
    def test_procesar_cola(self, mocker):
        with app.test_client() as client:
            payment_data = {'valor_pagado': 100, 'medio_pago_id': 1, "facturacion_id": 1, "es_excepcion": False}

            mocker.patch('src.service.service.PaymentService.update_invoice_state', return_value=1)

            payment_service.procesar_cola(payment_data)
            
    def test_update_invoice(self, mocker):
        with app.test_client() as client:
            mocker.patch('src.service.service.requests.patch', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            payment_service.update_invoice_state(1, "pagado")
            