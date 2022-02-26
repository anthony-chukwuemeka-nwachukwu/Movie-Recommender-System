from operator import index
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from src import db
from src.models.movie import Movie, movie_schemas
from src.forms.search import SearchForm
from .home import index

search = Blueprint('search', __name__)


@search.route('/search', methods=['POST', 'GET'])
def search_movie():
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.query.data
        return render_template(url_for('home.index', form=form))
    return render_template(url_for('home.index', form=form))

