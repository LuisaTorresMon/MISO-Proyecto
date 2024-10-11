from ..models.model import Person, PersonSchema, User, UserSchema, db
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_current_user, get_jwt
from ..errors.errors import IncorrectUserOrPasswordException, UserAlreadyExistException

user_schema = UserSchema()
person_schema = PersonSchema()

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
        
    def get_person_by_identity(self, identity_type, identity_number):
        
        person = Person.query.filter_by(tipo_identificacion=identity_type, numero_identificacion=identity_number).first()        
        return person_schema.dump(person)
