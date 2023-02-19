# Book-shop (BookShelf)
I decided to make an online bookstore.
The main feature is that the user can choose any of the offered books and make a payment.
Technology stack:
- Python/Flask/Flask-SQLALchemy
- PostgreSQL
- API
- HTML/CSS

![image](https://user-images.githubusercontent.com/119871133/219946656-92fe3356-a3f8-48e0-b80b-974bc0a8b2e9.png)
# Books
Books are the main thing in a bookstore. All information about them is contained in SQL database.

Books are output to the html template as an list. The "dataclasses" library helps us a little with this. And it looks something like this:

```
@dataclass
class BookView:
    name: str
    description: str
    author: str
    image_link: str
    price: int
    url: str = ''


@app.route("/", methods = ["GET","POST"])
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
```

We abbreviate the title of some books and we can see the full information on the page of the book.
As well as the fields: description and author. The link to the picture is also stored in the database.
In order to add a book if necessary, we would just need to add it to the database, but not make changes in the code.

![image](https://user-images.githubusercontent.com/119871133/219947384-f5e2ca50-b56e-4209-a59c-13cb2e964a77.png)

In the store tab, we can see a list of all available books. Which we also pass as one list. And with the help of a Jinja
we display each of them on the page.

```
  <div class="shop_container">
        {% for i in book %}
            <div class="product">
                <p class="book_name">{{i.name}}</p>  <a href=""></a>

                <a href="{{i.url}}">
                    <img class="img" src={{i.image_link}}>
                </a>
                
                <a href="{{i.url}}">
                    <button class="button__buy">buy</button>
                </a>
                <p class="book_price">{{i.price}} $</p>
            </div>
        {% endfor %}
    </div>
```

When you click on any book, a page appears with full information about it, as well as the ability to buy.
![image](https://user-images.githubusercontent.com/119871133/219947835-b533eee6-4fac-442f-8268-1cd451c2c319.png)

All books open on the same html template. Depending on which book we clicked , the program gets an ID and displays
all the data about the desired book on the page.

You don't need to create many html templates for this. AND we can choose the book we want.

![image](https://user-images.githubusercontent.com/119871133/219948010-27af3dbc-0197-4a28-87c1-eff109241710.png)

## Login and Registration
We need to be a logged in user so that the "Buy it" button allows us to proceed to payment. 
The @login_required decorator helps us with this.

So we have to log in.

![image](https://user-images.githubusercontent.com/119871133/219948565-be32d7ad-ca82-4206-8a18-c5853f1e7c9a.png)

We can register if we don't have an account.

The Flask Login library helps us with this. In order to register, we need to enter a unique login, as well as a password and repeat it.
The password is hashed using the function generate_password_hash(). The data puts into the SQL database "bookshelf" in the table "person".

The program will issue a flash warning if the fields are not filled, or the passwords do not match.

When logging, the data entered by the user is checked against the data that the database contains. If successful, the user logs into the
account. In case of failure, it displays flash warnings about incorrect data.

Let`s create a new user!
![image](https://user-images.githubusercontent.com/119871133/219948965-0e7d574d-67d7-44c1-8680-bbbe8d2cdeca.png)
We can see the new data in the database.

After we log into the account, we may notice small changes. The site greets us by our name. The login and registration buttons that were 
no longer needed have disappeared, and instead of them, a "logout" button has appeared.

![image](https://user-images.githubusercontent.com/119871133/219949114-afc5bc15-0fa6-410d-bc28-faf7a251a1ad.png)

## Payment
So now we can go and buy the book what we need. 

After clicking on the buy button. We will be redirected to the payment page using the Fondy service.

![image](https://user-images.githubusercontent.com/119871133/219949651-ac261924-8cc1-4d08-8c50-07ea7e8d0bd7.png)

The service will help us make payment depending on the selected book.

![image](https://user-images.githubusercontent.com/119871133/219949880-5b7ef473-3556-484c-a2b1-bc2e7dd32044.png)

( The payment was made for test purposes and it is not real! )

### Realisation of it
We import Api and Checkout from cloudipsp lib.
```
from cloudipsp import Api, Checkout

@app.route("/payment/<int:id>",  methods = ["GET", "POST"]) 
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
```
More information about it you can find here : https://github.com/cloudipsp/python-sdk

# The main task

The main goal of this project was the rational use of data from the SQL database. All books are passed to the HTML template through 1 list 
and output using a loop. When you click on the book, a pre-made template opens, which displays the necessary data. Using a base.HTML to use as
a base (FOOTER-HEADER) in other HTML files. Change the behavior of the 
program depending on whether the user is logged in or not. Using the API to add a payment system.
