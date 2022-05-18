import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

gr_API_key = "IHK16b7ODRjS2TBA6dH2w"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

os.environ[
        "DATABASE_URL"] = "postgresql+psycopg2://postgres:admin@127.0.0.1:5432/ranger_books_87"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from reviews.core.views import core
from reviews.users.views import users
from reviews.book_reviews.views import reviews

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(reviews)