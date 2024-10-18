from datetime import datetime, timedelta
from flask import jsonify, request, make_response
import requests
from .base_command import BaseCommannd
from src.models.model import Contract, Plan, db, ContractSchema, ContractGetJsonSchema

contract_schema = ContractSchema()

class Update(BaseCommannd):
    
    def __init__(self, data_contract):
        self.empresa_id = data_contract.get('empresa_id')
        self.new_plan_id = data_contract.get('new_plan_id')
    
    def execute(self):
        contract = Contract.query.filter_by(empresa_id=self.empresa_id).first()
        if not contract:
            return make_response(jsonify({"error": "El contrato no existe"}), 404)
        
        new_plan = Plan.query.filter_by(id=self.new_plan_id).first()
        if not new_plan:
            return make_response(jsonify({"error": "El nuevo plan no existe"}), 404)
        
        contract.plan_id = self.new_plan_id

        db.session.commit()

        schema = ContractGetJsonSchema()
        contract_data = schema.dump(contract)

        return jsonify(contract_data), 200
    