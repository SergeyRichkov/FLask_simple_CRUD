import os
from pprint import pprint

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy(app)
import models, routes

migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@127.0.0.1:5433/postgres'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:flask@0.0.0.0:5432/flask_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False

