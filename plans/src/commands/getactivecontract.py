from .base_command import BaseCommannd
from flask import jsonify
from src.models.model import Plan, Contract, db, ContractGetJsonSchema

class GetActiveContract(BaseCommannd):

    def __init__(self, empresa_id):
        self.empresa_id = empresa_id

    def execute(self):
        active_contract = Contract.query.filter_by(empresa_id=self.empresa_id, es_activo=True).first()
        if not active_contract:
            
            return jsonify({"error": "No hay contratos activos para esta empresa"}), 404

        schema = ContractGetJsonSchema()
        contract_data = schema.dump(active_contract)
        
        plan = Plan.query.filter(Plan.id == active_contract.plan_id).first()
        
        contract_data['precio_plan'] = plan.precio

        return jsonify(contract_data), 200