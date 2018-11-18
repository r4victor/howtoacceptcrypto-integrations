import os
import hmac

from flask import request, abort
import requests

from .db import db


API_KEY = os.getenv('COINBASE_COMMERCE_API_KEY')
if API_KEY is None:
    raise ValueError('COINBASE_COMMERCE_API_KEY is not set')


WEBHOOK_SECRET = os.getenv('COINBASE_COMMERCE_WEBHOOK_SECRET')
if WEBHOOK_SECRET is None:
    raise ValueError('COINBASE_COMMERCE_WEBHOOK_SECRET is not set')


CREATE_INVOICE_ENDPOINT = 'https://api.commerce.coinbase.com/charges'


def create_invoice(order, redirect_url):
    headers = {
        'X-CC-Api-Key': API_KEY,
        'X-CC-Version': '2018-03-22'
    }
    data = {
        'name': order['item']['name'],
        'description': order['item']['code'],
        'pricing_type': 'fixed_price',
        'local_price': {
            'amount': order['item']['price'].decimal_repr(),
            'currency': order['item']['price'].currency.code
        },
        'redirect_url': redirect_url,
        'cancel_url': redirect_url
    }
    response = requests.post(CREATE_INVOICE_ENDPOINT, headers=headers, json=data)
    if response.status_code is not 201:
        return None
    response_data = response.json()['data']
    invoice = {
        'id': response_data['id'],
        'status': 'created',
        'url': response_data['hosted_url']
    }
    db.create_invoice(invoice)
    return invoice


def handle_callback():
    provided_signature = request.headers.get('X-CC-Webhook-Signature')
    expecetd_signarure = hmac.digest(WEBHOOK_SECRET.encode(), request.get_data(), 'sha256').hex()
    if provided_signature != expecetd_signarure:
        abort(401)

    event = request.json['event']
    db.update_invoice(
        event['data']['id'],
        status=event['type'].split(':')[1]
    )
    return 'Thank you, Coinbase Commerce, for the free of charge service!'
