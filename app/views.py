from flask import Blueprint, redirect


bp = Blueprint('app', __name__)


@bp.route('/')
def index():
    return redirect('https://github.com/r4victor/howtoacceptcrypto-integrations')

