from . import app, db
from dataclasses import dataclass
from cloudipsp import Api, Checkout
from flask import render_template, redirect, url_for, request, flash
from flask_login import  login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from proccess.models import Book, person
from moduls.row_data_moduls import log_request

@dataclass
class BookView:
    name: str
    description: str
    author: str
    image_link: str
    price: int
    url: str = ''

@app.route("/")
@log_request
def main_page():
    books = Book.query.limit(3).all()
    book_views = []
    for book in books:
        book_views.append(BookView(
            name=f'{book.name[:10]}...' if len(book.name) > 10 else book.name,
            description="",
            author="",
            image_link=book.image_link,
            price=book.price,
            url=url_for('book_page', id=book.id),
        ))
    return render_template('index.html', book=book_views)



@app.route("/shop", methods = ["GET","POST"])
@log_request
def shop():

    books = Book.query.limit(6).all()
    book_views = []
    for book in books:
        book_views.append(BookView(
            name=f'{book.name[:10]}...' if len(book.name) > 10 else book.name,
            description="",
            author="",
            image_link=book.image_link,
            price=book.price,
            url=url_for('book_page', id=book.id),
        ))
   
    return render_template('shop.html', book=book_views)

@app.route("/books/<int:id>",  methods = ["GET", "POST"])
@log_request
def book_page(id):
    book = Book.query.filter_by(id = id).first()

    return render_template("book_page.html", book=book)

@app.route("/payment/<int:id>",  methods = ["GET", "POST"])
@log_request
@login_required
def pay(id):
    book = Book.query.filter_by(id = id).first()

    api = Api(merchant_id=1396424,
          secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(book.price) +"00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route("/login", methods = ["GET","POST"])
@log_request
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
@log_request
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
@log_request
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.after_request
@log_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response

@app.route("/contact")
@log_request
def contact():
    return render_template('contact.html')