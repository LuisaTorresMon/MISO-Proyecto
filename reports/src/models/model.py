import uuid
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

Base = declarative_base()

db = SQLAlchemy()

class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_reporte = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_final = db.Column(db.DateTime, nullable=True)
    estado_id = db.Column(db.Integer, nullable=True)
    tipo_id = db.Column(db.Integer, nullable=True)
    canal_id = db.Column(db.Integer, nullable=True)    

class ReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Report
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()
