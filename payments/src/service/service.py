from ..models.models import Payment, PaymentSchema, db

payment_schema = PaymentSchema()

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
        
        return payment_schema.dump(payment)
    
    def procesar_cola(self, invoice):
        
        self.es_excepcion = invoice.get('es_excepcion')
        
        if self.es_excepcion is True:
            payment = db.session.query(Payment).filter_by(facturacion_id=self.facturacion_id).first()
            if payment:
                if payment.intentos <= 4:
                    payment.intentos += 1
                    db.session.commit()                
                    raise Exception("Este es un mensaje de excepcion de procesamiento de cola")
                else:
                    self.create_payment(invoice)
        else:
            self.create_payment(invoice)
            
    def get_payments(self):
      payments = db.session.query(Payment).all()
            
      invoices_schema = [payment_schema.dump(payment) for payment in payments]
      return invoices_schema

