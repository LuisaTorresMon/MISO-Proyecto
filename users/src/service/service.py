from ..models.model import User, TipoUsuario, Empresa, ProductPerson, Product, Person, PersonSchema, ProductSchema, UserSchema, EmpresaSchema, db
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, create_access_token, get_current_user, get_jwt
from ..errors.errors import IncorrectUserOrPasswordException, UserAlreadyExistException, BadRequestException, ResourceNotFound
from ..validators.validator import UserValidator
import logging
from sqlalchemy import or_

user_schema = UserSchema()
product_schema = ProductSchema()
empresa_schema = EmpresaSchema()
persona_schema = PersonSchema()

class UserService():

    def __init__(self):
        pass

    def create_user(self, user):
        self.id_persona = user.get('id_person')
        self.id_empresa = Empresa.query.first().id
        self.id_tipousuario = user.get('id_typeuser')
        self.username = user.get('username')
        self.password = user.get('password').encode('utf-8')

        if self.id_persona is None and self.id_empresa is None and self.id_tipousuario is None:
            raise BadRequestException

        else:
            if self.id_persona is not None:
                if str(self.id_persona).strip() != "":
                    try:
                        int( self.id_persona)
                    except ValueError:
                        raise BadRequestException

            if self.id_empresa is not None:
                if str(self.id_empresa).strip() != "":
                    try:
                        int( self.id_empresa)
                    except ValueError:
                        raise BadRequestException
                
            if self.id_tipousuario is not None:
                if str(self.id_tipousuario).strip() != "":
                    try:
                        int( self.id_tipousuario)
                    except ValueError:
                        raise BadRequestException

        user = User.query.filter_by(nombre_usuario=self.username).first()

        if user:
            raise UserAlreadyExistException

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password, salt)

        new_user = User(
            id_persona=self.id_persona,
            id_empresa=self.id_empresa,
            id_tipousuario=self.id_tipousuario,
            nombre_usuario=self.username,
            contrasena=hashed_password.decode('utf-8')
        )

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user)

    def signIn(self, user):
        username = user.get('username')
        password = user.get('password')
        technology = user.get('technology')

        if technology == 'WEB':
            stored_user = User.query.filter_by(nombre_usuario=username).first()
            if stored_user.tipo_usuario.id == 3:
                stored_user = None
        elif technology == 'MOBILE':
            stored_user = User.query.filter_by(nombre_usuario=username).join(User.tipo_usuario).filter(or_(TipoUsuario.id == 3, TipoUsuario.id == 1)).first()
        else:
            raise BadRequestException

        if stored_user is None:
            raise IncorrectUserOrPasswordException

        if not bcrypt.checkpw(password.encode('utf-8'), stored_user.contrasena.encode('utf-8')):
            raise IncorrectUserOrPasswordException

        additional_claims = {
            "id": stored_user.id,
            "id_person": stored_user.id_persona,
            "id_company": stored_user.id_empresa,
            "user_type": stored_user.tipo_usuario.tipo
        }

        token_de_acceso = create_access_token(identity=str(stored_user.id), additional_claims=additional_claims)
        return {
            "token": token_de_acceso
        }
        
    def create_person(self, person):
                
        name = person.get('name') 
        lastname = person.get('lastname')
        email = person.get('email')
        identity_type = person.get('identity_type')
        identity_number = person.get('identity_number')
        cellphone = person.get('cellphone')
        
        new_person = self.get_person_by_identity(identity_type, identity_number)

        if not new_person:
            new_person = Person(
                nombres = name,
                apellidos = lastname,
                tipo_identificacion = identity_type,
                numero_identificacion = identity_number,
                telefono = cellphone,
                correo_electronico = email
            )
        
            db.session.add(new_person)
            db.session.commit()
        
        return persona_schema.dump(new_person) 
    
    def update_person(self, person):
                
        name = person.get('name') 
        lastname = person.get('lastname')
        email = person.get('email')
        identity_type = person.get('identity_type')
        identity_number = person.get('identity_number')
        cellphone = person.get('cellphone')
        
        existing_person = self.get_person_by_identity(identity_type, identity_number)

        existing_person.nombres = name
        existing_person.apellidos = lastname
        existing_person.tipo_identificacion = identity_type
        existing_person.numero_identificacion = identity_number
        existing_person.telefono = cellphone
        existing_person.correo_electronico = email
        
        db.session.commit()        
        return persona_schema.dump(existing_person) 
    
    def get_agents_by_company(self, company_id):       
        id_type_user = 2; 
        agents = User.query.filter_by(id_empresa=company_id, id_tipousuario=id_type_user).all()    
        agents_data = []
        for agent in agents:

            agent_data = {
                'id': agent.id,
                'nombre_usuario': agent.nombre_usuario,
                'numero_identificacion': agent.persona.numero_identificacion,
                'nombre_completo': f"{agent.persona.nombres} {agent.persona.apellidos}",
                'correo_electronico': agent.persona.correo_electronico,
                'telefono': agent.persona.telefono
            }
            
            agents_data.append(agent_data)
       
        return agents_data
        
    def get_person_by_identity(self, identity_type, identity_number):        
        person = Person.query.filter_by(tipo_identificacion=identity_type, numero_identificacion=identity_number).first()        
        return person

    def get_company_by_id(self, id):
        company = Empresa.query.filter(Empresa.id==id).first()
        if company:
            return company
        else:
            raise ResourceNotFound
        
    def get_person_by_id(self, id):
        person = Person.query.filter_by(id=id).first()
        if person:
            return person
        else:
            raise ResourceNotFound

    def get_user_by_id(self, id):
        user = db.session.query(User).filter_by(id=id).first()
        if user:
            user_data = user_schema.dump(user)
            if user.persona:
                user_data['persona'] = persona_schema.dump(user.persona)
            return user_data
        else:
            raise ResourceNotFound
        
    def get_user_by_username(self, username):
        user = db.session.query(User).filter(User.nombre_usuario==username).first()
        if user:
            return user_schema.dump(user)
        else:
            raise ResourceNotFound

    def get_products_by_person(self, person_id):
        products = db.session.query(Product).join(ProductPerson).filter(ProductPerson.id_persona == person_id).all()
        products_schema = [product_schema.dump(product) for product in products]
        
        return products_schema

    def register_client(self, user):
        user_type = 'client'
        id_user_type = 1

        UserValidator.validate_registration_data(user, user_type)

        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombre_empresa = user.get('nombre_empresa')
        tipo_identificacion = user.get('tipo_identificacion')
        numero_identificacion = user.get('numero_identificacion')
        sector = user.get('sector')
        telefono = user.get('telefono')
        pais = user.get('pais')
        email = user.get('email')

        nueva_empresa = Empresa(
            nombre_empresa = nombre_empresa,
            tipo_identificacion = tipo_identificacion,
            numero_identificacion = numero_identificacion,
            sector = sector,
            telefono = telefono,
            pais = pais,
            email = email
        )

        db.session.add(nueva_empresa)
        db.session.commit()

        user_data = {
            "username": nombre_usuario,
            "password": contrasena,
            "id_company": nueva_empresa.id,
            "id_typeuser": id_user_type
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Cliente registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "empresa": nueva_empresa.nombre_empresa,
            "id_company": nueva_empresa.id
        })

    def register_agent(self, user):
        user_type = 'agent'
        id_user_type = 2

        UserValidator.validate_registration_data(user, user_type)

        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombres = user.get('nombres')
        apellidos = user.get('apellidos')
        tipo_identificacion = user.get('tipo_identificacion')
        numero_identificacion = user.get('numero_identificacion')
        telefono = user.get('telefono')
        correo_electronico = user.get('correo_electronico')
        id_empresa = user.get('id_empresa')

        logging.debug(id_empresa)

        nuevo_agente = Person(
            nombres =nombres,
            apellidos = apellidos,
            tipo_identificacion = tipo_identificacion,
            numero_identificacion = numero_identificacion,
            telefono = telefono,
            correo_electronico = correo_electronico
        )

        db.session.add(nuevo_agente)
        db.session.commit()

        user_data = {
            "username": nombre_usuario,
            "password": contrasena,
            "id_company": id_empresa,
            "id_typeuser": id_user_type,
            "id_person": nuevo_agente.id
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Cliente registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "empresa": nuevo_agente.nombres
        })
        
    def register_user(self, user):
        user_type = 'user'
        id_user_type = 3

        UserValidator.validate_registration_data(user, user_type)

        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombres = user.get('nombres')
        apellidos = user.get('apellidos')
        tipo_identificacion = user.get('tipo_identificacion')
        numero_identificacion = user.get('numero_identificacion')
        telefono = user.get('telefono')
        correo_electronico = user.get('correo_electronico')
        id_empresa = user.get('id_empresa')

        logging.debug(id_empresa)

        nuevo_agente = Person(
            nombres =nombres,
            apellidos = apellidos,
            tipo_identificacion = tipo_identificacion,
            numero_identificacion = numero_identificacion,
            telefono = telefono,
            correo_electronico = correo_electronico
        )

        db.session.add(nuevo_agente)
        db.session.commit()

        user_data = {
            "username": nombre_usuario,
            "password": contrasena,
            "id_typeuser": id_user_type,
            "id_person": nuevo_agente.id
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Usuario registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "empresa": nuevo_agente.nombres
        })
    