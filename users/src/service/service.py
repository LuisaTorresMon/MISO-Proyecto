from ..models.model import User, UserSchema, Empresa, EmpresaSchema, Persona, PersonaSchema, db
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_current_user, get_jwt
from ..errors.errors import IncorrectUserOrPasswordException, UserAlreadyExistException, BadRequestException
from ..validators.validator import UserValidator
user_schema = UserSchema()
empresa_schema = EmpresaSchema()
persona_schema = PersonaSchema()

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

    def register_client(self, user):
        UserValidator.validate_registration_data(user)

        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombre_empresa = user.get('nombre_completo')
        email = user.get('email')
        tipo_identificacion = user.get('tipo_documento')
        numero_identificacion = user.get('numero_documento')
        sector = user.get('sector')
        telefono = user.get('telefono')
        pais = user.get('pais')

        nueva_empresa = Empresa(
            nombre_empresa = nombre_empresa,
            email = email,
            tipo_identificacion = tipo_identificacion,
            numero_identificacion = numero_identificacion,
            sector = sector,
            telefono = telefono,
            pais = pais
        )

        db.session.add(nueva_empresa)
        db.session.commit()

        user_data = {
            "username": nombre_usuario,
            "password": contrasena,
            "id_company": nueva_empresa.id
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Cliente registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "empresa": nombre_empresa
        })
    
    def register_agent(self, user):

        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombre_agente = user.get('nombre_completo')
        tipo_identificacion = user.get('tipo_identificacion')
        numero_identificacion = user.get('numero_identificacion')
        telefono = user.get('telefono')
        email = user.get('correo_electronico')

        nuevo_agente = Persona(
            nombre_completo = nombre_agente,
            tipo_identificacion = tipo_identificacion,
            numero_identificacion = numero_identificacion,
            telefono = telefono,
            correo_electronico = email
        )

        db.session.add(nuevo_agente)
        db.session.commit()

        user_data = {
            "username": nombre_usuario,
            "password": contrasena,
            "id_company": nuevo_agente.id
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Agente registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "agente": nuevo_agente.nombre_completo
        })
    