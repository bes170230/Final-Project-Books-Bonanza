import os
import csv

from flask import Flask
from models import Book
from app import db

os.environ[
        "DATABASE_URL"] = "postgresql://tyuvmczxhkxerv:9ed58427a78a6c50b892d188a4c443cb92fe9fe14289a88b37feefa28c90f53e@ec2-3-231-82-226.compute-1.amazonaws.com:5432/d5ogq7gr3o1ffa"

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def import_books(csv_path):
    f = open(csv_path)
    reader = csv.reader(f)
    header_line = True
    for isbn,title,author,year in reader:
        if header_line:
            header_line = False
            continue
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()