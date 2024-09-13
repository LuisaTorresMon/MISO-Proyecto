from ..models.models import Invoice, InvoiceSchema, db

invoice_schema = InvoiceSchema()


class InvoiceService():
    def create_invoice(self, invoice):
        self.referencia_pago = invoice.get('referencia_pago')
        self.valor_pagar = invoice.get('valor_pagar')
        self.fecha_pago = invoice.get('fecha_pago')
        self.estado_factura = invoice.get('estado_factura')
        self.empresa_id = invoice.get('empresa_id')
        
        invoice = Invoice(             
            referencia_pago = self.referencia_pago,
            valor_pagar = self.valor_pagar,
            fecha_pago = self.fecha_pago,
            estado_factura =self.estado_factura,
            empresa_id = self.empresa_id
        )
        
        db.session.add(invoice)
        db.session.commit()
        
        return invoice_schema.dump(invoice)
    
    def get_invoices(self):
      invoices = db.session.query(Invoice).all()
            
      invoices_schema = [invoice_schema.dump(invoice) for invoice in invoices]
      return invoices_schema

