from app.db import Database


class ExtendedDatabase(Database):
    def get_invoice(self, invoice_id):
        if not self.db_connection.exists(f'{self.processor}:invoice:{invoice_id}'):
            return None
        return {
            'id': invoice_id,
            'status': int(self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:status').decode()),
            'status_text': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:status_text').decode(),
            'amount': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:amount').decode(),
            'address': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:address').decode(),
            'url': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:url').decode(),
            'qrcode_url': self.db_connection.get(f'{self.processor}:invoice:{invoice_id}:qrcode_url').decode()
        }


db = ExtendedDatabase('CoinPayments')