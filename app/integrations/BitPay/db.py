from app.db import Database


class ExtendedDatabase(Database):
    def get_invoice(self, invoice_id):
        if not self.db_connection.exists(f'{self.processor}:invoice:{invoice_id}'):
            return None
        return {
            'id': invoice_id,
            'status': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:status').decode(),
            'url': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:url').decode()
        }


db = ExtendedDatabase('BitPay')