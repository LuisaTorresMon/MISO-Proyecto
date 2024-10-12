from ..models.model import Person, Product, ProductPerson, PersonSchema, User, UserSchema, ProductSchema, db
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_current_user, get_jwt
from ..errors.errors import IncorrectUserOrPasswordException, UserAlreadyExistException, BadRequestException

user_schema = UserSchema()
person_schema = PersonSchema()
person_schema = PersonSchema()
product_schema = ProductSchema()

class UserService():

    def __init__(self):
        pass

    def create_user(self, user):
        self.id_persona = user.get('id_person')
        self.id_empresa = user.get('id_company')
        self.username = user.get('username')
        self.password = user.get('password').encode('utf-8')

        if self.id_persona is None and self.id_empresa is None:
            raise BadRequestException
        elif self.id_persona is not None and self.id_empresa is not None:
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



        user = User.query.filter_by(nombre_usuario=self.username).first()

        if user:
            raise UserAlreadyExistException

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password, salt)

        new_user = User(
            id_persona=self.id_persona,
            id_empresa=self.id_empresa,
            nombre_usuario=self.username,
            contrasena=hashed_password.decode('utf-8')
        )

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user)

    def signIn(self, user):
        username = user.get('username')
        password = user.get('password')

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(nombre_usuario=username).first()

        if user is None:
            raise IncorrectUserOrPasswordException

        if not bcrypt.checkpw(password.encode('utf-8'), user.contrasena.encode('utf-8')):
            raise IncorrectUserOrPasswordException

        additional_claims = {
            "id": user.id,
            "id_person": user.id_persona,
            "id_company": user.id_empresa
        }
        token_de_acceso = create_access_token(identity=user.id, additional_claims=additional_claims)

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
        
        return person_schema.dump(new_person) 
    
    def update_person(self, person):
                
        name = person.get('name') 
        lastname = person.get('lastname')
        email = person.get('email')
        identity_type = person.get('identity_type')
        identity_number = person.get('identity_number')
        cellphone = person.get('cellphone')
        
        existing_person = self.get_person_by_identity(identity_type, identity_number)

        existing_person.nombres = name,
        existing_person.apellidos = lastname,
        existing_person.tipo_identificacion = identity_type,
        existing_person.numero_identificacion = identity_number,
        existing_person.telefono = cellphone,
        existing_person.correo_electronico = email
        
        db.session.commit()        
        return person_schema.dump(existing_person) 
        
    def get_person_by_identity(self, identity_type, identity_number):        
        person = Person.query.filter_by(tipo_identificacion=identity_type, numero_identificacion=identity_number).first()        
        return person
    
    def get_products_by_person(self, person_id):
        products = db.session.query(Product).join(ProductPerson).filter(ProductPerson.id_persona == person_id).all()
        products_schema = [product_schema.dump(product) for product in products]
        
        return products_schema


