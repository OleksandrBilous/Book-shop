from dataclasses import dataclass
from cloudipsp import Api, Checkout
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "shhh, don't tell this password"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/bookshelf'
db =SQLAlchemy(app)

migrate = Migrate(app, db)
manager = LoginManager(app)

@dataclass
class BookView:
    name: str
    description: str
    author: str
    image_link: str
    price: int
    url: str = ''


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
    return person.query.get(int(user_id))


@app.route("/", methods = ["GET","POST"])
def main_page():
    knigs = Book.query.limit(3).all()
    book_views = []
    for kniga in knigs:
        book_views.append(BookView(
            name=f'{kniga.name[:10]}...' if len(kniga.name) > 10 else kniga.name,
            description="",
            author="",
            image_link=kniga.image_link,
            price=kniga.price,
            url=url_for('book_page', id=kniga.id),
        ))
    return render_template('index.html', kniga=book_views)



@app.route("/shop", methods = ["GET","POST"])
def shop():

    knigs = Book.query.limit(6).all()
    book_views = []
    for kniga in knigs:
        book_views.append(BookView(
            name=f'{kniga.name[:10]}...' if len(kniga.name) > 10 else kniga.name,
            description="",
            author="",
            image_link=kniga.image_link,
            price=kniga.price,
            url=url_for('book_page', id=kniga.id),
        ))
   
    return render_template('shop.html', kniga=book_views)

@app.route("/books/<int:id>",  methods = ["GET", "POST"])
def book_page(id):
    kniga = Book.query.filter_by(id = id).first()

    return render_template("book_page.html", kniga=kniga)

@app.route("/payment/<int:id>",  methods = ["GET", "POST"]) 
@login_required
def pay(id):
    kniga = Book.query.filter_by(id = id).first()

    api = Api(merchant_id=1396424,
          secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(kniga.price) +"00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route("/login", methods = ["GET","POST"])
def login_page():
    phone_number = request.form.get('number')
    password = request.form.get('password')

    if phone_number and password:
        user = person.query.filter_by(phone_number=phone_number).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill the fields')
    return render_template('login.html')

@app.route("/register", methods = ["GET","POST"])
def register():
    name = request.form.get('Fname')
    surname = request.form.get('surname')
    number = request.form.get('number')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (number or password or password2): 
            flash('Please, fill all fields!')
            return redirect(url_for('register'))
        elif password != password2:   
            flash('Passwords are not equal!')
            return redirect(url_for('register'))
        else:
            hash_pwd = generate_password_hash(password)
            new_user = person(name = name, surname = surname, phone_number=number, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
 
    return render_template('register.html')

@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response

@app.route("/contact")
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True)