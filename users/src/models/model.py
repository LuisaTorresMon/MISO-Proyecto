import uuid
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import bcrypt

Base = declarative_base()

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_persona = db.Column(db.Integer)
    id_empresa = db.Column(db.Integer)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    es_activo = db.Column(db.Boolean, server_default="true", nullable=False)

class Empresa(db.Model):
    __tablename__ = 'empresa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_empresa = db.Column(db.String(200))
    email = db.Column(db.String(200))
    tipo_identificacion = db.Column(db.Integer)
    numero_identificacion = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    telefono = db.Column(db.Integer)
    pais = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class Persona(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(200))
    tipo_identificacion = db.Column(db.Integer)
    numero_identificacion = db.Column(db.String(100))
    telefono = db.Column(db.Integer)
    correo_electronico = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        include_fk = True
        exclude = ("contrasena", )
    id = fields.Integer()

class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

class PersonaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Persona
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

def cargar_datos_iniciales():
    if User.query.count() == 0:
        password = "123456"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        users = [
            User(id_persona=1, id_empresa=None, nombre_usuario="sa", contrasena=hashed_password.decode("utf-8"))  # Almacena como bytes
        ]

        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Datos iniciales cargados en la tabla users")
    else:
        print("La tabla users ya tiene datos")
        