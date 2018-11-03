import os

TESTING = False

SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('No secret key set for Flask application')