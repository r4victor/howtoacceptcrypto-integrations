from flask import Blueprint, render_template, redirect, url_for, abort, request

from app.data import customers, items
from .db import db
from . import api


bp = Blueprint(
    'BTCPay',
    __name__,
    url_prefix='/btcpay',
    static_folder='static',
    template_folder='templates'
)


processor = {
    'name': 'BTCPay',
    'github_path': 'BTCPay',
    'website_url': 'https://github.com/btcpayserver/btcpayserver'
}


@bp.route('/')
def page():
    return render_template(
        'BTCPay.html',
        processor=processor,
        item=items['pipe']
    )


@bp.route('/checkout/')
def checkout():
    return render_template(
        'BTCPay_checkout.html',
        processor=processor,
        item=items['pipe'],
        customer=customers['Holmes']
    )


@bp.route('/new_order/', methods=['POST'])
def new_order():
    new_order = {
        'id': db.get_next_order_id(),
        'item': items['pipe'],
        'customer': customers['Holmes']
    }
    db.create_order(new_order)
    invoice = api.create_invoice(
        new_order,
        url_for('.callback', _external=True),
        url_for('.order', order_id=new_order['id'], _external=True)
    )
    db.update_order(new_order['id'], invoice_id=invoice['id'])
    return redirect(invoice['url'])


@bp.route('/order/<int:order_id>/')
def order(order_id):
    order = db.get_order(order_id)
    if order is None:
        abort(404)
    invoice = db.get_invoice(order['invoice_id'])
    return render_template(
        'BTCPay_order.html',
        processor=processor,
        item=items['pipe'],
        order=order,
        invoice=invoice
    )


bp.add_url_rule('/callback/', 'callback', api.handle_callback, methods=['POST'])