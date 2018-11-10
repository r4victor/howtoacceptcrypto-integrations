import os
import requests

from flask import request

from .db import db


TOKEN = os.getenv('BITPAY_TOKEN')
if TOKEN is None:
    raise ValueError('BITPAY_TOKEN is not set')


CREATE_INVOICE_ENDPOINT = 'https://test.bitpay.com/invoices'


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
    response = requests.post(CREATE_INVOICE_ENDPOINT, data=data)
    if response.status_code is not 200:
        return None
    response_data = response.json()['data']
    invoice = {
        'id': response_data['id'],
        'status': response_data['status'],
        'url': response_data['url']
    }
    db.create_invoice(invoice)
    return invoice


def handle_callback():
    invoice = request.json
    db.update_invoice(
        invoice['id'],
        status=invoice['status']
    )
    return 'Thank you, BitPay, for amazing API!'
