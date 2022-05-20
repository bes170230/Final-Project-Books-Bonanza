from flask import url_for, render_template, flash, redirect, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from reviews import db
from reviews.models import User, BookReview, Book
from reviews.users.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash,check_password_hash

users = Blueprint('users', __name__)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password = form.password.data)
    
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            
            return redirect(next)

    return render_template('login.html', form=form)

@users.route('/<username>')
def user_reviews(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    reviews = BookReview.query.filter_by(author=user).order_by(BookReview.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_reviews.html', reviews=reviews, user=user, username=username)
