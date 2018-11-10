from flask import Blueprint, render_template, redirect, url_for, abort, request

from app.data import customers, items
from .db import db
from . import api


bp = Blueprint(
    'CoinGate',
    __name__,
    url_prefix='/coingate',
    static_folder='static',
    template_folder='templates'
)


processor = {
    'name': 'CoinGate',
    'github_path': 'CoinGate',
    'website_url': 'https://coingate.com'
}


@bp.route('/')
def page():
    return render_template(
        'CoinGate.html',
        processor=processor,
        item1=items['pipe']
    )


@bp.route('/checkout/')
def checkout():
    return render_template(
        'CoinGate_checkout.html',
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
    return redirect(url_for('.order', order_id=new_order['id']))


@bp.route('/order/<int:order_id>/')
def order(order_id):
    order = db.get_order(order_id)
    if order is None:
        abort(404)
    invoice = db.get_invoice(order['invoice_id'])
    return render_template(
        'CoinGate_order.html',
        processor=processor,
        item=items['pipe'],
        order=order,
        invoice=invoice
    )


bp.add_url_rule('/callback/', 'callback', api.handle_callback, methods=['POST'])