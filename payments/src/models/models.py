from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'pago'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_pagado = db.Column(db.Double, nullable=False)
    facturacion_id = db.Column(db.Integer, nullable=False)
    medio_pago_id = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    intentos = db.Column(db.Integer, nullable=False, default=1) 

    
class PaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()