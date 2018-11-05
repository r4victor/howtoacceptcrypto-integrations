import redis


class Database:
    def __init__(self, processor):
        self.processor = processor

    @classmethod
    def init_app(cls, app):
        cls.db_connection = redis.StrictRedis(
            app.config['REDIS_HOST'],
            app.config['REDIS_PORT'],
            db=0
        )

    def get_next_order_id(self):
        return self.db_connection.incr('last_order_id', amount=1)

    def create_order(self, order):
        # Create empty record, we don't need to ship anything
        print(order["id"])
        return self.db_connection.set(f'{self.processor}:order:{order["id"]}', '', ex=86400)

    def update_order(self, order_id, **kwargs):
        for k, v in kwargs.items():
            self.db_connection.set(f'{self.processor}:order:{order_id}:{k}', v, ex=86400)

    def get_order(self, order_id):
        if not self.db_connection.exists(f'{self.processor}:order:{order_id}'):
            return None
        return {
            'id': order_id,
            'invoice_id': self.db_connection.get(f'{self.processor}:order:{order_id}:invoice_id')
        }
        