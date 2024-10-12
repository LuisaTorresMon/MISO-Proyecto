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
    
class Person(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)
    tipo_identificacion = db.Column(db.String(50), nullable=False)
    numero_identificacion = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    correo_electronico = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    
class Product(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_producto = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class ProductPerson(db.Model):
    __tablename__ = 'persona_producto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_adquisicion = db.Column(db.Date, nullable=False)
    id_persona = db.Column(db.Integer, nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        include_fk = True
        exclude = ("contrasena", )
    id = fields.Integer()
    
class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True  
        
class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True  

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