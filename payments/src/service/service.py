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
    
    def get_payments(self):
      payments = db.session.query(Payment).all()
            
      invoices_schema = [payment_schema.dump(payment) for payment in payments]
      return invoices_schema

