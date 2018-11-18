import os
import requests

from flask import request

from .db import db


API_KEY = os.getenv('COINBASE_COMMERCE_API_KEY')
if API_KEY is None:
    raise ValueError('COINBASE_COMMERCE_API_KEY is not set')


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
    event = request.json['event']
    db.update_invoice(
        event['data']['id'],
        status=event['type'].split(':')[1]
    )
    return 'Thank you, Coinbase Commerce, for the free of charge service!'
