from ..models.model import User, UserSchema, Empresa, EmpresaSchema, db
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_current_user, get_jwt
from ..errors.errors import IncorrectUserOrPasswordException, UserAlreadyExistException
user_schema = UserSchema()
empresa_schema = EmpresaSchema()

class UserService():

    def __init__(self):
        pass

    def create_user(self, user):
        self.username = user.get('username')
        self.password = user.get('password').encode('utf-8')

        user = User.query.filter_by(nombre_usuario=self.username).first()

        if user:
            raise UserAlreadyExistException

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password, salt)

        new_user = User(
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

        # Generar el token JWT
        additional_claims = {"usuario": "usuario"}
        token_de_acceso = create_access_token(identity=user.id, additional_claims=additional_claims)

        return {
            "mensaje": "Inicio de sesión exitoso",
            "token": token_de_acceso,
            "id": user.id,
            "username": user.nombre_usuario  # Corrige esto si el atributo es 'nombre_usuario'
        }
    
    def register_client(self, user):
        nombre_usuario = user.get('usuario')
        contrasena = user.get('contrasena')
        nombre_empresa = user.get('nombre_completo')
        tipo_identificacion = user.get('tipo_documento')
        numero_identificacion = user.get('numero_documento')
        sector = user.get('sector')
        telefono = user.get('telefono')
        pais = user.get('pais')

        nueva_empresa = Empresa(
            nombre_empresa = nombre_empresa,
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
            "password": contrasena
        }
        new_user = self.create_user(user_data)

        return jsonify({
            "message": "Cliente registrado exitosamente.",
            "usuario": new_user['nombre_usuario'],
            "empresa": nombre_empresa
        })