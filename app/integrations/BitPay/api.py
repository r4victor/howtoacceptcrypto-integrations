import os
import json

import requests
from flask import request, abort

from .db import db


TOKEN = os.getenv('BITPAY_TOKEN')
if TOKEN is None:
    raise ValueError('BITPAY_TOKEN is not set')


CREATE_INVOICE_ENDPOINT = 'https://test.bitpay.com/invoices'


def create_invoice(order, callback_url, redirect_url):
    callback_token = os.urandom(16).hex()
    data = {
        'token': TOKEN,
        'price': order['item']['price'].decimal_repr(),
        'currency': order['item']['price'].currency.code,
        'orderId': order['id'],
        'itemDesc': order['item']['name'],
        'itemCode': order['item']['code'],
        'notificationURL': callback_url,
        'redirectURL': redirect_url,
        'buyer': {
            'name': f'{order["customer"]["first_name"]} {order["customer"]["last_name"]}',
            'address1': order['customer']['address'],
            'locality': order['customer']['city'],
            'postalCode': order['customer']['zip_code'],
            'country': order['customer']['country'],
        },
        'posData': json.dumps({'callback_token': callback_token})
    }
    response = requests.post(CREATE_INVOICE_ENDPOINT, json=data)
    if response.status_code is not 200:
        return None
    response_data = response.json()['data']
    invoice = {
        'id': response_data['id'],
        'token': callback_token,
        'status': response_data['status'],
        'url': response_data['url']
    }
    db.create_invoice(invoice)
    return invoice


def handle_callback():
    data = request.json
    callback_token = json.loads(data['posData'])['callback_token']
    invoice_token = db.get_invoice_token(data['id'])
    if callback_token != invoice_token:
        abort(401)
    db.update_invoice(
        data['id'],
        status=data['status']
    )
    return 'Thank you, BitPay, for amazing API!'
