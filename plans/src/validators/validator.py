from src.errors.errors import TokenNoEnviado, TokenVencido, CamposFaltantes, SizeInvalido, OfferInvalida, ErrorUUID
from src.commands.create import Create
import uuid

campos_requeridos = ['postId', 'description', 'size', 'fragile', 'offer']

class ValidadorOfertas():

    def validar_request_creacion(self, headers, data):
        token_encabezado = headers.get('Authorization')
        
        self.validar_token_enviado(token_encabezado)
        self.validar_token_vencido(token_encabezado)
        self.validar_campos_requeridos(data)
        self.validar_size_enviado(data.get('size'))
        self.validar_offer_enviada(data.get('offer'))
        
        return True

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
                raise CamposFaltantes
    
    def validar_size_enviado(self, data):
        valid_values = ["LARGE", "MEDIUM", "SMALL"]
        if data not in valid_values:
            raise SizeInvalido
    
    def validar_offer_enviada(self, data):
        if data < 0:
            raise OfferInvalida
    
    def validar_uuid(self, field):
        try:
            uuid.UUID(field)
            return
        except ValueError:
            raise ErrorUUID