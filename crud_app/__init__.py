from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)

from crud_app import routes, models

migrate = Migrate(app, db)

app.config.from_object(Config)


