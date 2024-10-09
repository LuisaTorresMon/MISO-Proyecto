from src.errors.errors import TokenNoEnviado, TokenVencido, BadRequestException, EmailInvalido, TelefonoNoNumerico, PassNoCoincide, PassNoValido
import re

campos_requeridos = ['username', 'password']

class UserValidator():

    def validar_request_creacion(self, headers, data):
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        return True

    def validar_listado(self, headers):
        
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        return True

    def validar_consulta(self, headers):
        
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        return True
        
    def validar_token_enviado(self, token):
        if token is None:
            raise TokenNoEnviado
    
    def validar_token_vencido(self, token):
        parts_token = token.split()
        if "fake" in parts_token[1]:
            raise TokenVencido
    
    @staticmethod
    def validate_registration_data(user):
        required_fields = [
            'usuario', 'contrasena', 'nombre_completo', 'tipo_documento',
            'numero_documento', 'sector', 'telefono', 'pais', 'confirmar_contrasena'
        ]
        for field in required_fields:
            if not user.get(field):
                raise BadRequestException(f"El campo {field} es obligatorio.")
        
        email = user.get('email')
        if not UserValidator.is_valid_email(email):
            raise EmailInvalido
        
        telefono = user.get('telefono')
        if not telefono.isdigit():
            raise TelefonoNoNumerico
        
        # Validación de coincidencia en la contraseña
        if user.get('contrasena') != user.get('confirmar_contrasena'):
            raise PassNoCoincide
        
        # Validación de formato de contraseña
        contrasena = user.get('contrasena')
        if not UserValidator.is_valid_password(contrasena):
            raise PassNoValido
    
    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)
    
    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True