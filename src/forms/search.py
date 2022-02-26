from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField, StringField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    query = SearchField(validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Search')

    