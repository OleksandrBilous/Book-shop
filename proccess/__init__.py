from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "shhh, don't tell this password"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/bookshelf'

db =SQLAlchemy(app)

migrate = Migrate(app, db)

from . import route