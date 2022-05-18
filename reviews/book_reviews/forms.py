from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    rating = RadioField('Please choose a rating:', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    text = TextAreaField('Share your thoughts about the book:')
    submit = SubmitField('Submit Review')