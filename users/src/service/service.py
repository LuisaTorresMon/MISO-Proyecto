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
        print(user)
        self.id_persona = user.get('id_person')
        self.id_empresa = user.get('id_company')
        self.id_tipousuario = user.get('id_typeuser')
        self.username = user.get('username')
        self.password = user.get('password').encode('utf-8')

        if self.id_persona is None and self.id_empresa is None and self.id_tipousuario is None:
            raise BadRequestException
        elif self.id_persona is not None and self.id_empresa is not None and self.id_tipousuario is not None:
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

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(nombre_usuario=username).first()

        if user is None:
            raise IncorrectUserOrPasswordException

        # Verificar la contraseña
        # No es necesario codificar user.contrasena nuevamente
        if not bcrypt.checkpw(password.encode('utf-8'), user.contrasena.encode('utf-8')):
            raise IncorrectUserOrPasswordException

        additional_claims = {
            "id": user.id,
            "id_person": user.id_persona,
            "id_company": user.id_empresa,
            "id_typeuser": user.id_tipousuario
        }
        token_de_acceso = create_access_token(identity=user.id, additional_claims=additional_claims)

        return {
            "token": token_de_acceso
        }

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
            "empresa": nueva_empresa.nombre_empresa
        })

    def register_agent(self, user):
        user_type = 'agent'
        id_user_type = 2

        UserValidator.validate_registration_data(user, user_type)

        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombre_completo = user.get('nombre_completo')
        tipo_identificacion = user.get('tipo_identificacion')
        numero_identificacion = user.get('numero_identificacion')
        telefono = user.get('telefono')
        correo_electronico = user.get('correo_electronico')

        nuevo_agente = Persona(
            nombre_completo = nombre_completo,
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
            "id_company": nuevo_agente.id,
            "id_typeuser": id_user_type
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Cliente registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "empresa": nuevo_agente.nombre_completo
        })

    def register_user(self, user):
        fullname = user.get('fullName')
        password = user.get("password")
        username = user.get("username")

        new_user_person = Persona(
            nombre_completo = fullname
        )

        db.session.add(new_user_person)
        db.session.commit()

        user_data = {
            "username": username,
            "password": password,
            "id_persona": new_user_person.id
        }

        print(user_data)
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Cliente registrado exitosamente.",
            "usuario": new_user['nombre_usuario']
        })
    