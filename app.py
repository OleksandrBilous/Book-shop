from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/bookshelf'
db =SQLAlchemy(app)

migrate = Migrate(app, db)
manager = LoginManager(app)

class Book (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(32))
    price = db.Column(db.Integer, nullable=False)
    image_link = db.Column(db.String)   

class person (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Order (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


@manager.user_loader
def load_user(user_id):
    return person.query.get(user_id)


@app.route("/", methods = ["GET","POST"])
def main_page():
    kniga = Book.query.filter_by(id = 3).first()
    print(kniga.id)
    print(kniga.name)
    print(kniga.description)
    print(kniga.author)
    print(kniga.price)
    print(kniga.image_link)
    return render_template('index.html', kniga=kniga)


if __name__ == '__main__':
    app.run(debug=True)