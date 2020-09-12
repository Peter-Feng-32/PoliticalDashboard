import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "delete-this-later"
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME') or 'admin'

    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD') or '1234'