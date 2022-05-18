from csv import unregister_dialect
from reviews import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from reviews import gr_API_key
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
    reviews = db.relationship('BookReview', backref='reviewer', lazy=True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)

    def __init__(self, title, text, user_id, rating):
        self.title = title
        self.text = text
        self.user_id = user_id 
        self.rating = rating

    def __repr__(self):
        return f"Review ID: {self.id} ; Date: {self.date}; Title: {self.title}; Rating: {self.rating}"

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    review_count = db.Column(db.Integer)
    average_score = db.Column(db.Float)
    gr_review_count = db.Column(db.Integer)
    gr_average_score = db.Column(db.Float)
    reviews = db.relationship("BookReview", backref="book", lazy=True)

    def __init__(self, isbn, title, author, year=None):
        # self.id   # get when inserted to db
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.average_score = 0
        self.review_count = 0
        self.gr_average_score, self.gr_review_count = get_gr_reviews_data(isbn)

    def add_review(self, user_id, rating, text):
        """Adds a review for this book object. returns true on success"""
        if len(BookReview.query.filter_by(book_isbn=self.isbn, user_id=user_id).all()) > 0:
            return False
        new_review = BookReview(book_isbn=self.isbn, user_id=user_id, rating=rating, text=text)
        db.session.add(new_review)
        self.review_count += 1  # add review to count
        self.sum_of_ratings += rating
        self.average_rating = (self.sum_of_ratings / self.review_count)  # calculate new average
        db.session.commit()
        return True

def get_gr_reviews_data(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": gr_API_key, "isbns": isbn})
    if res.status_code == 404:
        return None, None
    json = res.json()
    print("JSON File:" + str(json))
    print("Score:" + str(json["books"][0]["average_rating"]))
    print("Count:" + str(json["books"][0]["work_ratings_count"]))
    avg_rating = float(json["books"][0]["average_rating"])
    ratings_count = int(json["books"][0]["work_ratings_count"])
    return ratings_count, avg_rating