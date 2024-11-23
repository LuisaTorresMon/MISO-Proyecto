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
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    id_tipousuario = db.Column(db.Integer, db.ForeignKey('tipousuario.id'), nullable=False)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    es_activo = db.Column(db.Boolean, server_default="true", nullable=False)
    
    tipo_usuario = db.relationship('TipoUsuario', backref='usuarios')
    persona = db.relationship('Person', backref='usuarios')


    
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

class Empresa(db.Model):
    __tablename__ = 'empresa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_empresa = db.Column(db.String(200))
    email = db.Column(db.String(200))
    tipo_identificacion = db.Column(db.Integer)
    numero_identificacion = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    pais = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, server_default=func.now(), nullable=False)

class TipoUsuario(db.Model):
    __tablename__ = 'tipousuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(200))

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

class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

class TipoUsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TipoUsuario
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.String()

def cargar_datos_iniciales():
    
    automated_person = db.session.query(Person).filter_by(numero_identificacion="0000000001").first()
    ia_person = db.session.query(Person).filter_by(numero_identificacion="0000000002").first()
    person = db.session.query(Person).filter_by(numero_identificacion="1030661927").first()
    nueva_empresa = db.session.query(Empresa).filter_by(numero_identificacion="00000000").first()
    
    if not nueva_empresa:
        nueva_empresa = Empresa(
                nombre_empresa="Compañía de Prueba S.A.",
                email="contacto@compania.com",
                tipo_identificacion=1,  
                numero_identificacion="00000000",
                sector="Tecnología",
                telefono="+123456789",
                pais="Costa Rica"
        )
          
        db.session.add(nueva_empresa)
        db.session.commit()

    if not person:
            person = Person(
                nombres="test",
                apellidos="test",
                tipo_identificacion="1",
                numero_identificacion="1030661927",
                telefono="3142567890",
                correo_electronico="testuser@hotmail.com",
            )
            db.session.add(person)
            db.session.commit()
            print("Nueva persona creada.")
    else:
            print("La persona ya existe en la base de datos.")
            
    if not automated_person:
            automated_person = Person(
                nombres="agente",
                apellidos="automatico",
                tipo_identificacion="1",
                numero_identificacion="0000000001",
                telefono="3142567890",
                correo_electronico="automation_test@hotmail.com",
            )
            db.session.add(automated_person)
            db.session.commit()
            print("Nueva persona creada.")
    else:
            print("La persona ya existe en la base de datos.")

    if not ia_person:
            ia_person = Person(
                nombres="ia",
                apellidos="automatico",
                tipo_identificacion="2",
                numero_identificacion="0000000002",
                telefono="3142567890",
                correo_electronico="ia_test@hotmail.com",
            )
            db.session.add(ia_person)
            db.session.commit()
            print("Usuario IA creado")
    else:
            print("La persona ya existe en la base de datos.")
    
    if TipoUsuario.query.count() == 0:
        type_users = [
            TipoUsuario(tipo="cliente"),
            TipoUsuario(tipo="agente"),
            TipoUsuario(tipo="usuario")
        ]

        db.session.bulk_save_objects(type_users)
        db.session.commit()
        print("Datos iniciales cargados en la tabla TipoUsuario")
    else:
        print("La tabla TipoUsuario ya tiene datos")
        
    
    if User.query.count() == 0: 
        password = "123456"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        users = [
            User(id_empresa=nueva_empresa.id, id_tipousuario = 1, id_persona=person.id, nombre_usuario="sa", contrasena=hashed_password.decode("utf-8")),  
            User(id_empresa=nueva_empresa.id, id_tipousuario = 2, id_persona=automated_person.id, nombre_usuario="test_agent", contrasena=hashed_password.decode("utf-8")),
        ]

        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Datos iniciales cargados en la tabla users")

    else:
        print("La tabla users ya tiene datos")
        
    automation_agent = db.session.query(User).filter(User.nombre_usuario=="agente_automatico").first()
    if not automation_agent:
        automation_person = db.session.query(Person).filter(Person.numero_identificacion == '0000000001').first()
        automation_agent = User(id_empresa=None, 
                                id_persona=automation_person.id,
                                id_tipousuario = 2, 
                                nombre_usuario="agente_automatico", 
                                contrasena='1')
        
        db.session.add(automation_agent) 
        db.session.commit()

    ia_agent = db.session.query(User).filter(User.nombre_usuario == "agente_ia").first()
    if not ia_agent:
        ia_person = db.session.query(Person).filter(Person.numero_identificacion == '0000000002').first()
        ia_agent = User(id_empresa=None,
                                id_persona=ia_person.id,
                                id_tipousuario=2,
                                nombre_usuario="agente_ia",
                                contrasena='1')

        db.session.add(ia_agent)
        db.session.commit()
        