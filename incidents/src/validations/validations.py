import logging
from ..errors.errors import CamposFaltantes, BadRequestError, InvalidToken, ErrorService, TokenEmpty
from email_validator import validate_email, EmailNotValidError
import requests

class ValidatorIncidents():
    def validate_incident_data(self, nombre_cliente, 
                         apellido_cliente, 
                         correo_electronico_cliente, 
                         tipo_documento_cliente,
                         numero_documento_cliente,
                         celular_cliente,
                         tipo_incidencia,
                         canal_incidencia,
                         asunto_incidencia,
                         detalle_incidencia,
                         token):
        
        self.nombre_cliente = nombre_cliente
        self.apellido_cliente = apellido_cliente
        self.tipo_documento_cliente = tipo_documento_cliente
        self.numero_documento_cliente = numero_documento_cliente
        self.correo_electronico_cliente = correo_electronico_cliente
        self.celular_cliente = celular_cliente
        self.tipo_incidencia = tipo_incidencia
        self.canal_incidencia = canal_incidencia
        self.asunto_incidencia = asunto_incidencia
        self.detalle_incidencia = detalle_incidencia
        
        self.validar_token_enviado(token)
        self.validar_token_valido(token)
        self.validar_campos_requeridos()
        self.validar_formato_tamano_campos()
        
    def validar_campos_requeridos(self):
        if not self.nombre_cliente:
            raise CamposFaltantes("El campo nombre esta vacio, recuerda que es obligatorio")
        if not self.apellido_cliente:
            raise CamposFaltantes("El campo apellido esta vacio, recuerda que es obligatorio")   
        if not self.correo_electronico_cliente:
            raise CamposFaltantes("El campo correo electronico esta vacio, recuerda que es obligatorio")   
        if not self.tipo_documento_cliente:
            raise CamposFaltantes("El campo tipo de documento esta vacio, recuerda que es obligatorio")   
        if not self.numero_documento_cliente:
            raise CamposFaltantes("El campo numero de documento esta vacio, recuerda que es obligatorio")   
        if not self.celular_cliente:
            raise CamposFaltantes("El campo celular esta vacio, recuerda que es obligatorio")   
        if not self.tipo_incidencia:
            raise CamposFaltantes("El campo tipo de incidente esta vacio, recuerda que es obligatorio")    
        if not self.canal_incidencia:
            raise CamposFaltantes("El campo canal de incidente esta vacio, recuerda que es obligatorio")  
        if not self.asunto_incidencia:
            raise CamposFaltantes("El campo asunto de incidente esta vacio, recuerda que es obligatorio") 
        if not self.detalle_incidencia:
            raise CamposFaltantes("El campo detalle de incidente esta vacio, recuerda que es obligatorio")  
        
    def validar_formato_tamano_campos(self):
        self.validar_numero_de_documento()
        self.validar_celular()
        self.validar_correo_electronico()
        
    def validar_correo_electronico(self):
        try:
            validate_email(self.correo_electronico_cliente)
            print("El correo es válido.")
            return True
        except EmailNotValidError as e:
            raise BadRequestError('El correo electronico debe ser un correo valido')
        
    def validar_celular(self):
        if (not self.celular_cliente.isdigit()):
                raise BadRequestError('El celular debe ser un campo numerico')

    def validar_numero_de_documento(self):
        if self.tipo_documento_cliente == 'Cedula de cuidadania':
            if (not self.numero_documento_cliente.isdigit()) or (len(self.numero_documento_cliente) != 8 and len(self.numero_documento_cliente) != 10) :
                raise BadRequestError('El numero de documento cuando es de tipo Cedula de cuidadania, debe ser numerico y debe tener una longitud de 8 0 10 caracteres')
            
        if self.tipo_documento_cliente == 'NIT':
            if (len(self.numero_documento_cliente) != 12):
                raise BadRequestError('El numero de documento cuando es de tipo NIT, debe tener una longitud de 12 caracteres')
            elif(self.numero_documento_cliente[10] != '-'):
                raise BadRequestError('El numero de documento cuando es de tipo NIT, debe tener un guion (-) antes del ultimo digito')
        if self.tipo_documento_cliente == 'Cedula de extrangeria':
            if (len(self.numero_documento_cliente) != 12 or (not self.numero_documento_cliente.isdigit())):
                raise BadRequestError('El numero de documento cuando es de tipo Cedula de extrangeria, debe ser numerico y debe tener una longitud de 12 caracteres')
    
    def validar_token_valido(self, token):
            token_sin_bearer = token[len('Bearer '):]
            logging.debug(f"token sin bearer {token_sin_bearer}")

            url = 'http://users:3000/user/auth/validate-token'

            headers = {
                "Authorization": f"Bearer {token_sin_bearer}",
                      }

            response = requests.post(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            if response.status_code == 200:
                return response
            elif response.status_code == 401:
                raise InvalidToken('')
            else:
                raise ErrorService('')   
            
    def validar_token_enviado(self, token):
        if token is None:
            raise TokenEmpty('')