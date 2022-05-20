import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

nyt_API_key = "LaXSo7pKM96pAjW2UBYtQOKKnAGRKSdW"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

os.environ[
        "DATABASE_URL"] = "postgresql://tyuvmczxhkxerv:9ed58427a78a6c50b892d188a4c443cb92fe9fe14289a88b37feefa28c90f53e@ec2-3-231-82-226.compute-1.amazonaws.com:5432/d5ogq7gr3o1ffa"

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