import pytest
from src.main import app
from src.validators.validations import ValidatorInvoice
from src.error.errors import InvoiceGeneralIntegration

validator_invoice = ValidatorInvoice()

class TestValidator():
    
    @pytest.fixture 
    def client(self):
        with app.test_client() as client:
            yield client
            
    def test_valid_token_failure(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=403, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3" 
            
            with pytest.raises(InvoiceGeneralIntegration):
                validator_invoice.valid_token(token)
                
    def test_valid_token_success(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3" 
            
            validator_invoice.valid_token(token)
            
    def test_validate_token_sent(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            
            with pytest.raises(InvoiceGeneralIntegration):
                validator_invoice.validate_token_sent(None)
                
    def test_validate_token_sent_success(self, mocker):
        with app.test_client() as test_client:
            mocker.patch('src.validators.validations.requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {'respuesta': 'Token valido'}))
            token = "Bearer 0bbcb410-4263-49fd-a553-62e98eabd7e3" 

            validator_invoice.validate_token_sent(token)
            
    def test_validate_data_pay_without_invoice_id(self):
        with app.test_client() as test_client:

            with pytest.raises(InvoiceGeneralIntegration):
                validator_invoice.validate_data_pay('', 2)
                
    def test_validate_data_pay_without_payment_method_id(self):
        with app.test_client() as test_client:

            with pytest.raises(InvoiceGeneralIntegration):
                validator_invoice.validate_data_pay(2, '')
                
    def test_validate_data_pay_without_payment_method_id_success(self):
        with app.test_client() as test_client:

            validator_invoice.validate_data_pay(2, 1)
            
              