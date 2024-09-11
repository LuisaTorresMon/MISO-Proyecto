import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()

class Plan(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_plan = db.Column(db.String(100))
    precio = db.Column(db.Integer)

class PlanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plan
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

class PlanGetJsonSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    nombre_plan = fields.String()
    precio = fields.Integer()

def cargar_datos_iniciales():
    if Plan.query.count() == 0:
        planes = [
            Plan(nombre_plan="Plan Emprendedor", precio=100),
            Plan(nombre_plan="Plan Empresario", precio=200),
            Plan(nombre_plan="Plan Empresario Plus", precio=300)
        ]
        # Agregar los planes a la sesión
        db.session.bulk_save_objects(planes)
        db.session.commit()
        print("Datos iniciales cargados en la tabla Plan")
    else:
        print("La tabla Plan ya tiene datos")

