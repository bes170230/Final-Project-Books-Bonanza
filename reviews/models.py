from csv import unregister_dialect
from reviews import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from reviews import nyt_API_key
import requests
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, index=True)
    username = db.Column(db.String(60), unique=True, index=True)
    password_hash = db.Column(db.String(120))
    reviews = db.relationship('BookReview', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"

class BookReview(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)

    def __init__(self, book_isbn, username, rating, text):
        self.book_isbn = book_isbn
        self.username = username
        self.rating = rating
        self.text = text

    def __repr__(self):
        return f"Review ID: {self.id} ; Date: {self.date}; Title: {self.title}; Rating: {self.rating}"

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    review_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float)
    reviews = db.relationship("BookReview", backref="book", lazy=True)

    def __init__(self, isbn, title, author, year=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.average_rating = 0
        self.review_count = 0

    def add_review(self, username, rating, text):
        if len(BookReview.query.filter_by(book_isbn=self.isbn, username=username).all()) > 0:
            return False
        new_review = BookReview(book_isbn=self.isbn, username=username, rating=rating, text=text)
        db.session.add(new_review)
        db.session.commit()
        return True

def get_nyt_data():
    res = requests.get("http://api.nytimes.com/svc/books/v3/lists/full-overview.json", params={"api-key": nyt_API_key})
    if res.status_code == 404:
        return None
    json = res.json()
    print("Bestsellers in fiction:" + str(json["results"]["lists"][0]["books"]))
    print("Bestsellers in nonfiction:" + str(json["results"]["lists"][1]["books"]))
    
    return res.text