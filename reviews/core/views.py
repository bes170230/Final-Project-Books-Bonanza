from flask import request, render_template, Blueprint, redirect, url_for
from flask_login import current_user
from reviews.book_reviews.forms import SearchForm
from reviews.book_reviews.views import results

core = Blueprint('core', __name__)

@core.route('/', methods=['GET', 'POST'])
@core.route('/search', methods=['GET', 'POST'])
def index():
    user = current_user
    if current_user.is_authenticated:
        form = SearchForm()
        if form.validate_on_submit():  
            return results(form)
        else:
            return render_template('search.html', title='Home', user=user, form=form)
    else:
        return redirect(url_for('users.login'))

