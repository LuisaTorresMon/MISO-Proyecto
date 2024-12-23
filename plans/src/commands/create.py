from datetime import datetime, timedelta
from flask import jsonify, request
import requests
from .base_command import BaseCommannd
from src.models.model import Contract, Plan, db, ContractSchema, ContractGetJsonSchema
from sqlalchemy import update


contract_schema = ContractSchema()

class Create(BaseCommannd):
    
    def __init__(self, data_contract):
        self.plan_id = data_contract.get('plan_id')
        self.empresa_id = data_contract.get('empresa_id')

    def execute(self):
        
        update_stmt = update(Contract).where(Contract.empresa_id == f"{self.empresa_id}").values(es_activo=False)
        db.session.execute(update_stmt)
        db.session.commit()

        plan = Plan.query.filter_by(id=self.plan_id).first()
        if not plan:
            return jsonify({"error": "El plan no existe"}), 404

        new_contract = Contract (
            es_activo = True,
            plan_id = self.plan_id,
            empresa_id = self.empresa_id
        )

        db.session.add(new_contract)
        db.session.commit()

        schema = ContractGetJsonSchema()
        contract_data = schema.dump(new_contract)

        return contract_data

