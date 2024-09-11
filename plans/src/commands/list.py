from .base_command import BaseCommannd
from src.models.model import Plan, db, PlanSchema, PlanGetJsonSchema

plans_schema = PlanSchema()

class List(BaseCommannd):

    def execute(self):
        plans = db.session.query(Plan).all()
        schema = PlanGetJsonSchema(many=True)
        plans_data = schema.dump(plans)

        return plans_data
