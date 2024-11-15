from ..models.models import Invoice, InvoiceSchema, db
from ..utils.utils import CommonUtils
from ..error.errors import InvoiceGeneralIntegration
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import extract
from google.cloud import pubsub_v1
import google.auth
from dotenv import load_dotenv
from datetime import datetime
from weasyprint import HTML
import logging
import json
import calendar
import os
import requests
import random

invoice_schema = InvoiceSchema()
common_utils = CommonUtils()

load_dotenv('.env.template')       

projec_id = os.environ.get('PROJECT_ID', '')
tema_publicacion = os.environ.get('TOPIC_ID', '')

INCIDENT_URL = os.environ.get('INCIDENT_PATH')
PLAN_URL = os.environ.get('PLAN_PATH')
USER_URL = os.environ.get('USER_PATH')

CALL_CHANNEL_ID = 1
EMAIL_CHANNEL_ID = 2
MOBILE_APP_CHANNEL_ID = 3
DOLAR_EXCHANGE = 4300

class InvoiceService():
    
    def build_invoice_client(self, token, month, company_id):
               
        invoice = db.session.query(Invoice).filter(
            Invoice.empresa_id == company_id,
            extract('month', Invoice.fecha_pago) == month
        ).first()
        
        active_plan = self.get_active_plan_by_company(token, company_id)
        logging.debug(f"active_plan {active_plan}")

        if not active_plan:
            raise InvoiceGeneralIntegration(404, "No tienes un plan activo, por ende no se puede cargar la factura")
        
        initial_date_plan_string = active_plan['fecha_inicio_plan']
        initial_date_month = datetime.fromisoformat(initial_date_plan_string).month
                        
        if(initial_date_month > month):
            raise InvoiceGeneralIntegration(404, "El mes de busqueda es menor a la fecha de inicio de vigencia del plan")

        current_month = datetime.now().month
        if(current_month < month):
            raise InvoiceGeneralIntegration(404, "El mes de busqueda es mayor al mes actual")

        
        if(invoice):
            if(invoice.estado_factura == 'Pendiente'):
                price_data = self.get_price_data(token, month, active_plan)
                invoice = self.geerate_invoice(price_data['incident_calls_price'],
                                               price_data['incident_calls_count'],
                                               price_data['incident_calls_unit_value'],
                                               price_data['incident_email_price'],
                                               price_data['incident_email_count'],
                                               price_data['incident_email_unit_value'],
                                               price_data['incidents_mobile_app_price'],
                                               price_data['incidents_mobile_app_count'],
                                               price_data['incidents_mobile_app_unit_value'],
                                               active_plan['precio_plan'],
                                               price_data['total_price'],
                                               company_id,
                                               month,
                                               invoice
                                               )
        else:
            price_data = self.get_price_data(token, month, active_plan)
            invoice = self.geerate_invoice(price_data['incident_calls_price'],
                                               price_data['incident_calls_count'],
                                               price_data['incident_calls_unit_value'],
                                               price_data['incident_email_price'],
                                               price_data['incident_email_count'],
                                               price_data['incident_email_unit_value'],
                                               price_data['incidents_mobile_app_price'],
                                               price_data['incidents_mobile_app_count'],
                                               price_data['incidents_mobile_app_unit_value'],
                                               active_plan['precio_plan'],
                                               price_data['total_price'],
                                               company_id,
                                               month)   
            
        invoice_json_schema = invoice_schema.dump(invoice)
            
        return invoice_json_schema
               
                
    def get_price_data(self, token, month, active_plan):
        incidents_call = self.get_incidents_count_by_username(token, month, CALL_CHANNEL_ID)
        incidents_email = self.get_incidents_count_by_username(token, month, EMAIL_CHANNEL_ID)
        incidents_mobile_app = self.get_incidents_count_by_username(token, month, MOBILE_APP_CHANNEL_ID)
        
        incident_calls_price = incidents_call['total_price']
        logging.debug(incident_calls_price)
                
        incident_calls_count = incidents_call['incident_count']
        logging.debug(incident_calls_count)
        
        incident_calls_unit_value = incidents_call['channel_price']
        logging.debug(incident_calls_unit_value)

        incident_email_price = incidents_email['total_price']
        logging.debug(incident_email_price)
        
        incident_email_count = incidents_email['incident_count']
        logging.debug(incident_email_count)
        
        incident_email_unit_value = incidents_email['channel_price']
        logging.debug(incident_email_unit_value)
        
        incidents_mobile_app_price = incidents_mobile_app['total_price']
        logging.debug(incidents_mobile_app_price)
        
        incidents_mobile_app_count = incidents_mobile_app['incident_count']
        logging.debug(incidents_mobile_app_count)
        
        incidents_mobile_app_unit_value = incidents_mobile_app['channel_price']
        logging.debug(incidents_mobile_app_unit_value)
        
        price_plan = active_plan['precio_plan']
        logging.debug(price_plan)

        total_price = incident_calls_price + incident_email_price + incidents_mobile_app_price + price_plan
        logging.debug(total_price)
                    
        return {"incident_calls_price": incident_calls_price,
                "incident_calls_count": incident_calls_count,
                "incident_calls_unit_value": incident_calls_unit_value,
                "incident_email_price": incident_email_price,
                "incident_email_count": incident_email_count,
                "incident_email_unit_value": incident_email_unit_value,
                "incidents_mobile_app_price": incidents_mobile_app_price,
                "incidents_mobile_app_count": incidents_mobile_app_count,
                "incidents_mobile_app_unit_value": incidents_mobile_app_unit_value,
                "total_price": total_price}

    def get_company(self, token, company_id):

            url = f"{USER_URL}/company/{company_id}"

            headers = common_utils.obtener_token(token)

            response = requests.get(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 200:
                logging.debug(f"response.json() {response.json()}")
                return response.json()
            else:   
                return None

    def get_incidents_count_by_username(self, token, month, channel):

            url = f"{INCIDENT_URL}/channel/{channel}/{month}"

            headers = common_utils.obtener_token(token)

            response = requests.get(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 200:
                logging.debug(f"response.json() {response.json()}")
                return response.json()
            else:   
                return None
            
    def get_active_plan_by_company(self, token, company_id):

            url = f"{PLAN_URL}/get/{company_id}"

            headers = common_utils.obtener_token(token)

            response = requests.get(url, headers=headers)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 200:
                logging.debug(f"response.json() {response.json()}")
                return response.json()
            else:
                return None
    
    def geerate_invoice(self, 
                        incident_calls_price, 
                        incident_calls_count,
                        incident_calls_unit_value,
                        incident_email_price,
                        incident_email_count,                        
                        incident_email_unit_value,
                        incidents_mobile_app_price,
                        incidents_mobile_app_count,
                        incident_mobile_app_unit_value,
                        price_plan,
                        total_price,
                        company_id,
                        month,
                        invoice = None):
        
        referencia = self.generate_incident_code()
        
        if not invoice:
        
            pay_date = datetime(datetime.now().year, month, calendar.monthrange(datetime.now().year, month)[1], 23, 59, 00)      
        
            invoice = Invoice(   
                referencia_pago = referencia,
                fecha_pago = pay_date,
                estado_factura = 'Pendiente',
                empresa_id = company_id,
                incidencia_llamadas_precio_total = incident_calls_price,
                numero_incidencia_llamadas = incident_calls_count,
                valor_unitario_incidencia_llamada = incident_calls_unit_value,
                incidencia_correo_precio_total = incident_email_price,
                numero_incidencia_correo = incident_email_count,
                valor_unitario_incidencia_correo = incident_email_unit_value,
                incidencia_movil_precio_total = incidents_mobile_app_price,
                numero_incidencia_movil = incidents_mobile_app_count,
                valor_unitario_incidencia_movil = incident_mobile_app_unit_value,
                plan_precio_total = price_plan,
                valor_pagar = total_price
            )
        
            db.session.add(invoice)
            db.session.commit()
        else:
            invoice.valor_pagar = total_price
            invoice.incidencia_llamadas_precio_total = incident_calls_price
            invoice.numero_incidencia_llamadas = incident_calls_count
            invoice.valor_unitario_incidencia_llamada = incident_calls_unit_value
            invoice.incidencia_correo_precio_total = incident_email_price
            invoice.numero_incidencia_correo = incident_email_count
            invoice.valor_unitario_incidencia_correo = incident_email_unit_value
            invoice.incidencia_movil_precio_total = incidents_mobile_app_price
            invoice.numero_incidencia_movil = incidents_mobile_app_count
            invoice.valor_unitario_incidencia_movil = incident_mobile_app_unit_value
            invoice.plan_precio_total = price_plan
            invoice.valor_pagar = total_price
            invoice.fecha_actualizacion = datetime.now()
            
            db.session.commit()       
        
        return invoice
    
    
    def generate_incident_code(self):
        random_number = random.randint(1, 5000)
        incident_code = f"REF{random_number:02d}"
        
        logging.debug(f"incident code {incident_code}")
             
        return incident_code
            
    def send_invoice_pdf_by_email(self, token, email, invoice_id, lang):
        subject = ''
        content = ''
        
        invoice = db.session.query(Invoice).filter(Invoice.id == invoice_id).first()
        
        attached_pdf = self.get_invoice_pdf(token, invoice_id, lang)
        
        if(lang == 'es'):
            subject = f"Envio de factura con referencia {invoice.referencia_pago}"
            content = f"Se realiza el envio automatico de la factura con referencia {invoice.referencia_pago}, la encontrara adjunta en formato pdf"
        else:
            subject = f"Send invoice with reference {invoice.referencia_pago}"
            content = f"The invoice is sent automatically with the reference number {invoice.referencia_pago}, you will find it attached in pdf format"
        
        response = common_utils.send_email(email, subject, content, attached_pdf)
        
        print(f"email reposnse {response}")
        
        return response
            
    def get_invoice_pdf(self, token, invoice_id, lang):
        
      invoice = db.session.query(Invoice).filter(Invoice.id == invoice_id).first()
        
      company = self.get_company(token, invoice.empresa_id)  
      logging.debug(company)  
        
      invoice = db.session.query(Invoice).filter(Invoice.id == invoice_id).first()
      template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
      env = Environment(loader=FileSystemLoader(template_dir))
      
      logo_path = os.path.join(template_dir, 'logo.png')
      
      logging.debug(template_dir)
      
      template = ''
      if(lang == 'es'): 
        template = env.get_template("template_pdf_es.html")
      else:
        template = env.get_template("template_pdf_en.html") 
         
      emition_date = invoice.fecha_creacion.strftime("%d/%m/%Y")
      expiration_date = invoice.fecha_pago.strftime("%d/%m/%Y")

      rendered = template.render(invoice=invoice, company=company, logo_path=logo_path, dolar_exchange = DOLAR_EXCHANGE, emition_date=emition_date, expiration_date=expiration_date)
      
      pdf = HTML(string=rendered).write_pdf()
      return {'pdf': pdf, 'file_name': f"factura_{invoice.referencia_pago}"}
    
    def get_invoices(self):
      invoices = db.session.query(Invoice).all()
            
      invoices_schema = [invoice_schema.dump(invoice) for invoice in invoices]
      return invoices_schema
  
    def update_state_invoice(self, state, id_invoice):
        invoice = db.session.query(Invoice).filter(Invoice.id == id_invoice).first()
        
        invoice.estado_factura = state        
        db.session.commit()
        
        return invoice_schema.dump(invoice)        

    def pay_menthod_queue(self, invoice_id, payment_method_id):
        
        publisher = pubsub_v1.PublisherClient()
        
        invoice = db.session.query(Invoice).filter(Invoice.id == invoice_id).first()
        
        credentials, project = google.auth.default()
        logging.debug(f"Current account: {credentials.service_account_email}")
        
        logging.debug('Entrando a encolar')
        topic_path = publisher.topic_path(projec_id, tema_publicacion)
        
        booleano_aleatorio = random.choice([True, False])

        payment_json = json.dumps({
             'valor_pagado': invoice.valor_pagar,
             'medio_pago_id': payment_method_id,
             'facturacion_id': invoice.id,
             'es_excepcion': booleano_aleatorio
        })
        
        logging.debug(f"Entrando a encolar {payment_json}")

        future = publisher.publish(topic_path, payment_json.encode("utf-8"))
        future.result()
        logging.debug('Encolado')
