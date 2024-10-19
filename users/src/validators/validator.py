from src.errors.errors import TokenNoEnviado, RequiredFields, TokenVencido, BadRequestException, EmailInvalido, TelefonoNoNumerico, PassNoCoincide, PassNoValido
import re

campos_requeridos = ['username', 'password']
person_required_files = ['identityType','identityNumber']

class UserValidator():

    def validar_request_creacion(self, headers, data):
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        self.validar_campos_requeridos(data)
        
        return True

    def validate_query_person(self, identity_type, identity_number):
        if not identity_type or not identity_number:
            raise RequiredFields

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

    
    def validar_campos_requeridos(self, data):
        for campo in campos_requeridos:
            if campo not in data:
                raise RequiredFields
    
    
    @staticmethod
    def validate_registration_data(user, user_type):   
        required_fields_client = ['usuario', 'contrasena', 'nombre_empresa', 'tipo_identificacion', 'numero_identificacion', 'sector', 'telefono', 'pais', 
                                  'confirmar_contrasena', 'email']
        required_fields_agent = ['usuario', 'contrasena', 'nombres', 'apellidos', 'tipo_identificacion', 'numero_identificacion', 'telefono', 'confirmar_contrasena', 
                                 'correo_electronico']
        
        if user_type == 'client':
            required_fields = required_fields_client
        elif user_type == 'agent':
            required_fields = required_fields_agent

        for field in required_fields:
            if not user.get(field):
                print(f"El campo {field} está faltando o es inválido.")
                raise BadRequestException(f"El campo {field} es obligatorio.")
        
        if user.get('email'):
            email = user.get('email')
            if email is None or not UserValidator.is_valid_email(email):
                raise EmailInvalido("El formato del email no es válido")
        
        if user.get('correo_electronico'):
            correo_electronico = user.get('correo_electronico')
            if correo_electronico is None or not UserValidator.is_valid_email(correo_electronico):
                raise EmailInvalido("El formato del email no es válido")
        
        telefono = str(user.get('telefono'))
        if not telefono.isdigit():
            raise TelefonoNoNumerico("El campo de teléfono debe contener solo números")
        
        # Validación de coincidencia en la contraseña
        if user.get('contrasena') != user.get('confirmar_contrasena'):
            raise PassNoCoincide("Las contraseñas no coinciden")
        
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
    
