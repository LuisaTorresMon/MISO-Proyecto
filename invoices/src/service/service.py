from ..models.models import Invoice, InvoiceSchema, db
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import logging
import json
import os

invoice_schema = InvoiceSchema()

load_dotenv('.env.template')       

projec_id = os.environ.get('PROJECT_ID', '')
tema_publicacion = os.environ.get('TOPIC_ID', '')

publisher = pubsub_v1.PublisherClient()

class InvoiceService():
    def create_invoice(self, invoice):
        self.referencia_pago = invoice.get('referencia_pago')
        self.valor_pagar = invoice.get('valor_pagar')
        self.fecha_pago = invoice.get('fecha_pago')
        self.estado_factura = invoice.get('estado_factura')
        self.empresa_id = invoice.get('empresa_id')
        self.es_excepcion = invoice.get('es_excepcion')
        
        invoice = Invoice(             
            referencia_pago = self.referencia_pago,
            valor_pagar = self.valor_pagar,
            fecha_pago = self.fecha_pago,
            estado_factura =self.estado_factura,
            empresa_id = self.empresa_id
        )
        
        db.session.add(invoice)
        db.session.commit()
        
        self.encolar(invoice)        
        
        return invoice_schema.dump(invoice)
    
    def get_invoices(self):
      invoices = db.session.query(Invoice).all()
            
      invoices_schema = [invoice_schema.dump(invoice) for invoice in invoices]
      return invoices_schema

    def encolar(self, invoice):
        logging.debug('Entrando a encolar')
        topic_path = publisher.topic_path(projec_id, tema_publicacion)

        payment_json = json.dumps({
             'valor_pagado': invoice.valor_pagar,
             'medio_pago_id': 2,
             'facturacion_id': invoice.id,
             'es_excepcion': self.es_excepcion
        })
        
        logging.debug(f"Entrando a encolar {payment_json}")

        
        future = publisher.publish(topic_path, payment_json.encode("utf-8"))
        future.result()
        logging.debug('Encolado')
