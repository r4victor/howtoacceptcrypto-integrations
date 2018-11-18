import os

from flask import Flask
from .db import Database

from .integrations.bitpay.views import bp as bitpay_bp
from .integrations.CoinGate.views import bp as CoinGate_bp
from .integrations.CoinPayments.views import bp as CoinPayments_bp
from .integrations.Coinbase_Commerce.views import bp as Coinbase_Commerce_bp


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        env = os.getenv('FLASK_ENV')
        if env == 'production':
            app.config.from_pyfile('settings/prod.py')
        elif env == 'development':
            app.config.from_pyfile('settings/dev.py')
        else:
            raise ValueError('Unknown FLASK_ENV variable')
    else:
        app.config.from_mapping(test_config)

    Database.init_app(app)

    app.register_blueprint(bitpay_bp)
    app.register_blueprint(CoinGate_bp)
    app.register_blueprint(CoinPayments_bp)
    app.register_blueprint(Coinbase_Commerce_bp)

    return app
