from .base_command import BaseCommannd
from src.models.model import Plan, db, PlanSchema, PlanGetJsonSchema
from src.errors.errors import PlanNoExiste

plans_schema = PlanSchema()

class Get(BaseCommannd):
    def __init__(self, planId):
        self.planId = planId

    def execute(self):
        plan = db.session.query(Plan).filter(Plan.id == self.planId).first()

        if plan is None:
            raise PlanNoExiste

        schema = PlanGetJsonSchema()
        plan_data = schema.dump(plan)

        return plan_data
    