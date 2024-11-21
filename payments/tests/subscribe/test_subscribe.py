import pytest
from src.main import app
from unittest.mock import MagicMock
from google.auth.credentials import AnonymousCredentials 
from src.subcribe.subscribe import callback, subscribe
import json

class TestSubscribe():
    
    @pytest.fixture 
    def client(self):
      with app.test_client() as client:
        yield client
        
    def test_callback(self, mocker):
      with app.test_client() as test_client:
          
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
        mocker.patch('src.subcribe.subscribe.pubsub_v1.SubscriberClient')
        mocker.patch('src.main.threading.Thread')
 
        payment_data = {'valor_pagado': 100, 'medio_pago_id': 1, "facturacion_id": 1, "es_excepcion": False}
        payment_data_encoded = json.dumps(payment_data).encode('utf-8')
        
        mocker.patch('src.service.service.PaymentService.update_invoice_state', return_value=1)
          
        mock_message = MagicMock()
        mock_message.data = payment_data_encoded
          
        callback(mock_message)
        
    def test_callback(self, mocker):
      with app.test_client() as test_client:
          
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
        mocker.patch('src.subcribe.subscribe.pubsub_v1.SubscriberClient')
        mocker.patch('src.main.threading.Thread')
 
        payment_data = {'valor_pagado': 100, 'medio_pago_id': 1, "facturacion_id": 1, "es_excepcion": False}
        payment_data_encoded = json.dumps(payment_data).encode('utf-8')
        
        mocker.patch('src.service.service.PaymentService.update_invoice_state', return_value=1)
          
        mock_message = MagicMock()
        mock_message.data = payment_data_encoded
          
        callback(mock_message)
        
    def test_callback_exception(self, mocker):
      with app.test_client() as test_client:
          
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
        mocker.patch('src.subcribe.subscribe.pubsub_v1.SubscriberClient')
        mocker.patch('src.main.threading.Thread')
 
        payment_data = {'valor_pagado': 100, 'medio_pago_id': 1, "facturacion_id": 1, "es_excepcion": True}
        payment_data_encoded = json.dumps(payment_data).encode('utf-8')
        
        mocker.patch('src.service.service.PaymentService.update_invoice_state', return_value=1)
          
        mock_message = MagicMock()
        mock_message.data = payment_data_encoded
        
        with pytest.raises(Exception):
            callback(mock_message)


    def test_subscribe(self, mocker):
      with app.test_client() as test_client:
          
        mocker.patch('google.auth.default', return_value=(mocker.Mock(spec=AnonymousCredentials), 'project-id'))
        mocker.patch('src.subcribe.subscribe.pubsub_v1.SubscriberClient')
 
        subscribe()        


