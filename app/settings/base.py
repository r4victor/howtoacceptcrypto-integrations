import os

TESTING = False

SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('FLASK_SECRET_KEY is not set')

REDIS_HOST = os.getenv('REDIS_HOST')
if not REDIS_HOST:
    raise ValueError('REDIS_HOST is not set')

REDIS_PORT = os.getenv('REDIS_PORT')
if not REDIS_PORT:
    raise ValueError('REDIS_PORT is not set')