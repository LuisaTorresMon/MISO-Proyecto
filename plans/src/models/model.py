import uuid
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()

class Plan(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.Integer, primary_key=True)
    nombre_plan = db.Column(db.String(100))
    precio = db.Column(db.Integer)

class PlanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plan
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Integer()

class PlanGetJsonSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    nombre_plan = fields.String()
    precio = fields.Integer()

def cargar_datos_iniciales():
    if Plan.query.count() == 0:
        planes = [
            Plan(id=1, nombre_plan="Plan Emprendedor", precio=200),
            Plan(id=2, nombre_plan="Plan Empresario", precio=300),
            Plan(id=3, nombre_plan="Plan Empresario Plus", precio=500)
        ]
        # Agregar los planes a la sesión
        db.session.bulk_save_objects(planes)
        db.session.commit()
        print("Datos iniciales cargados en la tabla Plan")
    else:
        print("La tabla Plan ya tiene datos")

class Contract(db.Model):
    __tablename__ = 'contract'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_inicio_plan = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin_plan = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=365))
    es_activo = db.Column(db.Boolean)
    plan_id = db.Column(db.Integer)
    empresa_id = db.Column(db.String(100))

class ContractSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contract
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Integer()

class ContractGetJsonSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    fecha_inicio_plan = fields.DateTime()
    fecha_fin_plan = fields.DateTime()
    es_activo = fields.Boolean()
    plan_id = fields.String()
    empresa_id = fields.String()
