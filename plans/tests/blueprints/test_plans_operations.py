import pytest
from unittest.mock import patch
from src.commands.create import Create
from src.models.model import Plan, Contract
from src.main import app
from src.commands.update import Update
from src.commands.getactivecontract import GetActiveContract
from flask import jsonify
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_plan(mocker):
    return mocker.patch('src.models.model.Plan.query.filter_by')

@pytest.fixture
def mock_contract(mocker):
    return mocker.patch('src.models.model.Contract')

class TestPlans():

    def test_create_contract_success(self, mock_plan, mock_contract):
        with app.test_client() as test_client:
            mock_plan.return_value.first.return_value = Plan(id=1)
            mock_contract.return_value = Contract()

            data = {"plan_id": 1, "empresa_id": 1}
            create_command = Create(data)
            response = create_command.execute()

            assert response['plan_id'] == '1'
            assert response['empresa_id'] == 1

    def test_create_contract_plan_not_found(self, mock_plan):
        with app.test_client() as test_client:
            mock_plan.return_value.first.return_value = None

            data = {"plan_id": 999, "empresa_id": 1}
            create_command = Create(data)
            response, status_code = create_command.execute()

            assert status_code == 404
            assert response.json['error'] == "El plan no existe"
    
    def test_update_contract_success(self, mock_contract, mock_plan):
        with app.test_client() as test_client:
            mock_contract.return_value.first.return_value = Contract(plan_id=1)
            mock_plan.return_value.first.return_value = Plan(id=2)

            data = {"empresa_id": 1, "new_plan_id": 2}
            update_command = Update(data)
            response, status_code = update_command.execute()
            json_data = response.get_json()

            assert status_code == 200
            assert json_data["plan_id"] == '2'

    def test_update_contract_not_found(self, mock_contract):
        with app.test_client() as test_client:
            mock_contract.return_value.first.return_value = None

            data = {"empresa_id": 1, "new_plan_id": 4}
            update_command = Update(data)
            response = update_command.execute()
            status_code = response.status_code
            json_data = response.get_json()

            assert status_code == 404
            assert json_data['error'] == "El nuevo plan no existe"

    def test_update_plan_not_found(self, mock_contract, mock_plan):
        with app.test_client() as test_client:
            mock_contract.return_value.first.return_value = Contract(plan_id=1)
            mock_plan.return_value.first.return_value = None

            data = {"empresa_id": 1, "new_plan_id": 999}
            update_command = Update(data)
            response = update_command.execute()
            status_code = response.status_code
            json_data = response.get_json()

            assert status_code == 404
            assert json_data['error'] == "El nuevo plan no existe"
    
    def test_get_active_contract_success(self, mock_contract):
        with app.test_client() as test_client:
            mock_contract.return_value.first.return_value = Contract(empresa_id=1, plan_id=1)

            get_command = GetActiveContract(empresa_id=1)
            response, status_code = get_command.execute()

            assert status_code == 200
            assert response.json["empresa_id"] == 1
            assert response.json["plan_id"] == '2'

    def test_get_active_contract_not_found(self, mock_contract):
        with app.test_client() as test_client:
            mock_contract.return_value.first.return_value = None

            get_command = GetActiveContract(empresa_id=40)
            response, status_code = get_command.execute()

            assert status_code == 404
            assert response.json['error'] == "No hay contratos activos para esta empresa"
    
    def test_create_contract(self, mocker):
        with app.test_client() as test_client:
            mock_create = mocker.patch('src.commands.create.Create.execute', return_value=jsonify({"plan_id": 1, "empresa_id": 1}), status=201)

            data = {
                "plan_id": 1,
                "empresa_id": 1
            }

            response = test_client.post(
                        '/plan/contract',  
                        data=json.dumps(data),
                        content_type='application/json'
                    )

            assert response.status_code == 201
            assert response.json['plan_id'] == 1
            assert response.json['empresa_id'] == 1
    
    def test_update_contract(self, mocker):
        with app.test_client() as test_client:
            mock_update = mocker.patch('src.commands.update.Update.execute', return_value=(jsonify({"plan_id": 2}), 200))

            data = {
                "empresa_id": 1,
                "new_plan_id": 2
            }
            response = test_client.post('plan/update/contract', data=json.dumps(data),
                        content_type='application/json')

            assert response.status_code == 200
            assert response.json['plan_id'] == 2
    
    def test_get_active_contract(self, mocker):
        with app.test_client() as test_client:
            mock_get_active_contract = mocker.patch('src.commands.getactivecontract.GetActiveContract.execute', return_value=(jsonify({"empresa_id": 1, "plan_id": 1}), 200))

            response = test_client.get('plan/get/1')

            assert response.status_code == 200
            assert response.json['empresa_id'] == 1
            assert response.json['plan_id'] == 1

    def test_health_check(self):
        with app.test_client() as test_client:
            response = test_client.get('plan/ping')

            assert response.status_code == 200
            assert response.data == b'pong'
            