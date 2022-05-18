from sqlalchemy import func
from reviews.models import User, Book
from flask_login import login_required, current_user
from flask import redirect, render_template, flash, url_for, Blueprint
from reviews.book_reviews.forms import ReviewForm

reviews = Blueprint('reviews', __name__)

@login_required
@reviews.route('/results', methods=['GET'])
def results(form):
    search_str = form.data['search']
    search_str = search_str.lower()
    if search_str == '':
        return redirect(url_for('search'))
    else:
        results=[]
        results.extend(Book.query.filter(func.lower(Book.title).contains(func.lower(search_str))).all())
        results.extend(Book.query.filter(func.lower(Book.author).contains(func.lower(search_str))).all())
        if len(results) == 0:
            flash("No books found.")
            return redirect(url_for('core.index'))
        else:
            return render_template('results.html', results=results, title="Search Results")

@login_required
@reviews.route("/books/<string:isbn>", methods=['GET','POST'])
def book_page(isbn):
    book = Book.query.get(isbn)
    if book is None:
        flash("Book not found")
        return redirect(url_for('core.index'))
    form = ReviewForm()
    done = None
    if form.validate_on_submit():
        score = int(form.score.data)
        text = form.text.data
        user_name = current_user.username
        done = book.add_review(user=user_name, score=score, text=text)
        if not done:
            flash("Book already reviewed")
        else:
            flash("Review added")
    reviews = book.reviews
    return render_template("book.html", book=book, reviews=reviews, form=form, title="Book Page", success=success)


