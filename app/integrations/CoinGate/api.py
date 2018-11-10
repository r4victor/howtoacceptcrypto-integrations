import os
import requests

from flask import request

from .db import db


TOKEN = os.getenv('COINGATE_TOKEN')
if TOKEN is None:
    raise ValueError('COINGATE_TOKEN is not set')


CREATE_INVOICE_ENDPOINT = 'https://api-sandbox.coingate.com/v2/orders'


def create_invoice(order, callback_url, redirect_url):
    headers = {
        'Authorization': f'Token {TOKEN}'
    }
    data = {
        'order_id': order['id'],
        'price_amount': order['item']['price'].decimal_repr(),
        'price_currency': order['item']['price'].currency.code,
        'receive_currency': 'BTC',
        'title': order['item']['name'],
        'callback_url': callback_url,
        'cancel_url': redirect_url,
        'success_url': redirect_url,
    }
    response = requests.post(
        CREATE_INVOICE_ENDPOINT,
        headers=headers,
        data=data
    )
    if response.status_code is not 200:
        return None
    response_data = response.json()
    invoice = {
        'id': response_data['id'],
        'status': response_data['status'],
        'url': response_data['payment_url']
    }
    db.create_invoice(invoice)
    return invoice


def handle_callback():
    data = request.form
    db.update_invoice(
        data['id'],
        status=data['status']
    )
    return 'Thank you, CoinGate, for well-documented API!'
