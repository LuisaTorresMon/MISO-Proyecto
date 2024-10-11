from src.errors.errors import TokenNoEnviado, TokenVencido, RequiredFields
import uuid

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

    def validar_consulta(self, headers, offerId):
        
        token_encabezado = headers.get('Authorization')
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        self.validar_uuid(offerId)

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
    
    
