import logging
from ..errors.errors import RequiredFields, BadRequestError, InvalidToken, ErrorService, TokenEmpty
from email_validator import validate_email, EmailNotValidError
import requests

class ValidatorIncidents():
    def validate_incident_data(self, name_person, 
                         lastname_person, 
                         email_person, 
                         identity_type_person,
                         identity_number_person,
                         cellphone_person,
                         incident_type,
                         channel_incident,
                         subject_incident,
                         detail_incident,
                         token):
        
        self.name_person = name_person
        self.lastname_person = lastname_person
        self.identity_type_person = identity_type_person
        self.identity_number_person = identity_number_person
        self.email_person = email_person
        self.cellphone_person = cellphone_person
        self.incident_type = incident_type
        self.channel_incident = channel_incident
        self.subject_incident = subject_incident
        self.detail_incident = detail_incident
        
        self.validate_token_sent(token)
        self.valid_token(token)
        self.validar_campos_requeridos()
        self.validar_formato_tamano_campos()
        
    def validar_campos_requeridos(self):
        if not self.name_person:
            raise RequiredFields("El campo nombre esta vacio, recuerda que es obligatorio")
        if not self.lastname_person:
            raise RequiredFields("El campo apellido esta vacio, recuerda que es obligatorio")   
        if not self.email_person:
            raise RequiredFields("El campo correo electronico esta vacio, recuerda que es obligatorio")   
        if not self.identity_type_person:
            raise RequiredFields("El campo tipo de documento esta vacio, recuerda que es obligatorio")   
        if not self.identity_number_person:
            raise RequiredFields("El campo numero de documento esta vacio, recuerda que es obligatorio")   
        if not self.cellphone_person:
            raise RequiredFields("El campo celular esta vacio, recuerda que es obligatorio")   
        if not self.incident_type:
            raise RequiredFields("El campo tipo de incidente esta vacio, recuerda que es obligatorio")    
        if not self.channel_incident:
            raise RequiredFields("El campo canal de incidente esta vacio, recuerda que es obligatorio")  
        if not self.subject_incident:
            raise RequiredFields("El campo asunto de incidente esta vacio, recuerda que es obligatorio") 
        if not self.detail_incident:
            raise RequiredFields("El campo detalle de incidente esta vacio, recuerda que es obligatorio")  
        
    def validar_formato_tamano_campos(self):
        self.validar_numero_de_documento()
        self.validar_celular()
        self.validar_correo_electronico()
        
    def validar_correo_electronico(self):
        try:
            validate_email(self.email_person)
            print("El correo es válido.")
            return True
        except EmailNotValidError as e:
            raise BadRequestError('El correo electronico debe ser un correo valido')
        
    def validar_celular(self):
        if (not self.cellphone_person.isdigit()):
                raise BadRequestError('El celular debe ser un campo numerico')

    def validar_numero_de_documento(self):
        if self.identity_type_person == 'Cédula_Cuidadania':
            if (not self.identity_number_person.isdigit()) or (len(self.identity_number_person) != 8 and len(self.identity_number_person) != 10) :
                raise BadRequestError('El numero de documento cuando es de tipo Cedula de cuidadania, debe ser numerico y debe tener una longitud de 8 0 10 caracteres')
            
        if self.identity_type_person == 'Cédula_Extrangeria':
            if (len(self.identity_number_person) != 12 or (not self.identity_number_person.isdigit())):
                raise BadRequestError('El numero de documento cuando es de tipo Cedula de extranjeria, debe ser numerico y debe tener una longitud de 12 caracteres')
    
    def valid_token(self, token):
            token_sin_bearer = token[len('Bearer '):]
            logging.debug(f"token sin bearer {token_sin_bearer}")

            
            #url = 'http://users:3000/user/auth/validate-token'
            url = 'http://users-service/user/auth/validate-token'


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
            
    def validate_token_sent(self, token):
        if token is None:
            raise TokenEmpty('')