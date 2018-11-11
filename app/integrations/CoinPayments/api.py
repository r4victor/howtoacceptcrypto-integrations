import os
import requests
import hmac

from flask import request, abort

from .db import db


PUBLIC_KEY = os.getenv('COINPAYMENTS_PUBLIC_KEY')
if PUBLIC_KEY is None:
    raise ValueError('COINPAYMENTS_PUBLIC_KEY is not set')


PRIVATE_KEY = os.getenv('COINPAYMENTS_PRIVATE_KEY')
if PRIVATE_KEY is None:
    raise ValueError('COINPAYMENTS_PRIVATE_KEY is not set')


IPN_SECRET = os.getenv('COINPAYMENTS_IPN_SECRET')
if IPN_SECRET is None:
    raise ValueError('COINPAYMENTS_IPN_SECRET is not set')


API_ENDPOINT = 'https://www.coinpayments.net/api.php'


def create_invoice(order, callback_url):
    data = {
        'version': 1,
        'key': PUBLIC_KEY,
        'cmd': 'create_transaction',
        'amount': order['item']['price'].decimal_repr(),
        'currency1': order['item']['price'].currency.code,
        'currency2': 'LTCT',
        'buyer_email': order['customer']['email'],
        'buyer_name': f'{order["customer"]["first_name"]} {order["customer"]["last_name"]}',
        'item_name': order['item']['name'],
        'item_number': order['item']['code'],
        'ipn_url': callback_url
    }
    prepped_request = requests.Request('POST', API_ENDPOINT, data=data).prepare()
    signature = hmac.digest(PRIVATE_KEY.encode(), prepped_request.body.encode(), 'sha512').hex()
    prepped_request.headers['HMAC'] = signature
    with requests.Session() as session:
        response = session.send(prepped_request)

    if response.status_code is not 200:
        return None

    response_data = response.json()
    if response_data['error'] != 'ok':
        return None
    
    invoice = {
        'id': response_data['result']['txn_id'],
        'status': 0,
        'status_text': 'new',
        'amount': response_data['result']['amount'],
        'address': response_data['result']['address'],
        'url': response_data['result']['status_url'],
        'qrcode_url': response_data['result']['qrcode_url'],
    }
    db.create_invoice(invoice)
    return invoice


def handle_callback():
    provided_signature = request.headers.get('Hmac')
    expecetd_signarure = hmac.digest(IPN_SECRET.encode(), request.get_data(), 'sha512').hex()
    if provided_signature != expecetd_signarure:
        abort(401)

    data = request.form
    db.update_invoice(
        data['txn_id'],
        status=data['status'],
        status_text=data['status_text']
    )
    return 'Thank you, CoinPayments, for secure API!'
