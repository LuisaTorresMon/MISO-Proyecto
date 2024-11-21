from ..models.models import Payment, PaymentSchema, db
import logging, requests, os
from dotenv import load_dotenv

payment_schema = PaymentSchema()

load_dotenv('.env.template')
INVOICE_PATH = os.environ.get('INVOICE_PATH')

class PaymentService():
    def create_payment(self, invoice):
                
        self.valor_pagado = invoice.get('valor_pagado')
        self.facturacion_id = invoice.get('facturacion_id')
        self.medio_pago_id = invoice.get('medio_pago_id')
        
        payment = Payment(             
            valor_pagado = self.valor_pagado,
            facturacion_id = self.facturacion_id,
            medio_pago_id = self.medio_pago_id
        )
        
        db.session.add(payment)
        db.session.commit()
        
        self.update_invoice_state(self.facturacion_id, "Pagado")
        
        return payment_schema.dump(payment)
    
    def procesar_cola(self, invoice):
        
        self.es_excepcion = invoice.get('es_excepcion')
        self.facturacion_id = invoice.get('facturacion_id')
        
        if self.es_excepcion is True:
            payment = db.session.query(Payment).filter_by(facturacion_id=self.facturacion_id).first()
            if payment:
                if payment.intentos <= 5:
                    payment.intentos += 1
                    db.session.commit()                
                    raise Exception("Este es un mensaje de excepcion de procesamiento de cola")
            else:
                self.create_payment(invoice)
                raise Exception("Este es un mensaje de excepcion de procesamiento de cola")

        else:
            self.create_payment(invoice)
  
    def update_invoice_state(self, invoice_id, state):

            url = f"{INVOICE_PATH}update/{invoice_id}/{state}"
            logging.debug(f"url {url}")

            response = requests.patch(url)
            logging.debug(f"codigo de respuesta {response.text}")
            print(f"codigo de respuesta {response.status_code}")

            if response.status_code == 200:
                logging.debug(f"response.json() {response.json()}")
                return response.json()
            else:
                return None

