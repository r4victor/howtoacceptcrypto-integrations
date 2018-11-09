import os
import requests
import json

from flask import request

from .db import db


TOKEN = os.getenv('BITPAY_TOKEN')
if TOKEN is None:
    raise ValueError('BitPay token is not set')


def create_invoice(order, callback_url, redirect_url):
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
        }
    }
    response = requests.post('https://test.bitpay.com/invoices', data=data)
    if response.status_code is not 200:
        return None
    invoice = response.json()['data']
    db.create_invoice({
        'id': invoice['id'],
        'status': invoice['status'],
        'url': invoice['url']
    })
    return invoice


def handle_callback():
    invoice = request.json
    db.update_invoice(
        invoice['id'],
        status=invoice['status']
    )
    return 'Thank you, BitPay, for amazing API!'
