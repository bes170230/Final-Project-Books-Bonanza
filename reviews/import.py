import os
import csv

from flask import Flask
from models import Book
from app import db

os.environ[
        "DATABASE_URL"] = "postgresql+psycopg2://postgres:admin@127.0.0.1:5432/ranger_books_88"

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
        print(f"Adding a book titled \"{title}\" by {author}.")
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()

def main():
    print("Creating tables...")
    db.create_all()
    print("Tables created!")
    print("Importing books...")
    import_books("books.csv")
    print("Books imported!")

if __name__ == "__main__":
    with app.app_context():
        main()