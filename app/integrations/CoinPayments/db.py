from app.db import Database


class ExtendedDatabase(Database):
    def get_invoice(self, invoice_id):
        keys = ['id', 'status', 'status_text', 'amount', 'address', 'url', 'qrcode_url']
        invoice = self.get_invoice_data(invoice_id, *keys)
        invoice['status'] = int(invoice['status'])
        return invoice


db = ExtendedDatabase('CoinPayments')