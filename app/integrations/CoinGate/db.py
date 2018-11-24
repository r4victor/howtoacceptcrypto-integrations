from app.db import Database


class ExtendedDatabase(Database):
    def get_invoice(self, invoice_id):
        return self.get_invoice_data(invoice_id, 'id', 'token', 'status', 'url')

    def get_invoice_token(self, invoice_id):
        return self.get_invoice_data(invoice_id, 'token')['token']


db = ExtendedDatabase('CoinGate')