import  os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@127.0.0.1:5433/postgres'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://flask_user:flask@0.0.0.0:5432/flask_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JSON_AS_ASCII = False