from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Invoice(db.Model):
    __tablename__ = 'facturacion'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    referencia_pago = db.Column(db.String(100), nullable=False)
    valor_pagar = db.Column(db.Double, nullable=False)
    fecha_pago = db.Column(db.Date, nullable=True)
    estado_factura = db.Column(db.String(50), nullable=False)
    empresa_id = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    
class InvoiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()