from flask import Blueprint, render_template


bp = Blueprint(
    'bitpay',
    __name__,
    url_prefix='/bitpay',
    static_folder='',
    template_folder=''
)


@bp.route('/')
def page():
    return render_template('bitpay.html')