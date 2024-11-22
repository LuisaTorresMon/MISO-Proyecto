import os
from dotenv import load_dotenv
from os import environ
from ..errors.errors import InvoiceGeneralIntegration
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import logging
import base64

FROM_EMAIL='proyectouniandes19@gmail.com'

class CommonUtils():
    def obtener_token(self, token):
        
        token_sin_bearer = token[len('Bearer '):]
        logging.debug(f"token sin bearer {token_sin_bearer}")
        
        headers = {
           "Authorization": f"Bearer {token_sin_bearer}",
        }
        return headers
    
    def send_email(self, email_destination, subject, content, attached=None):
        
        load_dotenv('.env.template')         
        sengrid_token = environ.get('SENGRID_TOKEN')
        
        logging.debug(email_destination)
        logging.debug(subject)
        logging.debug(content)
        logging.debug(sengrid_token)
        
        sg = SendGridAPIClient(sengrid_token)
        
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=email_destination,
            subject=subject,
            html_content=f"<p>{content}</p>"
        )       
        
        if(attached):
            
            with open(attached, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
            pdf_encoded = base64.b64encode(pdf_data).decode('utf-8')

            file_name = os.path.basename(attached)
            
            attached_email = Attachment(
                FileContent(pdf_encoded),
                FileName(file_name),
                FileType("application/pdf"),
                Disposition("attachment")
            )

            message.attachment = attached_email
            
        try:
            response = sg.send(message)
            logging.debug('Enviado con exito')
            return {"status_code": response.status_code}
    
        except Exception as e:
            logging.debug(e)
            #raise InvoiceGeneralIntegration(500, "Error a la hora de enviar el correo")
            raise (500, "Error a la hora de enviar el correo")
        