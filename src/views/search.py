import base64
from operator import index
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from src import db
from src.models.movie import Movie, movie_schemas
from src.forms.search import SearchForm
from .index import index
from src.param import signed_in, no_of_movie_per_genre, no_imdb_genres

search = Blueprint('search', __name__)


@search.route('/search', methods=['POST', 'GET'])
def search_movie():
    form = SearchForm()
    if form.validate_on_submit():
        #get_movies()
        search_term = form.query.data
        print(search_term)
        return render_template(url_for('home.index', form=form))
    return render_template(url_for('home.index', form=form))
    #url_for( 'index.home', user_name=session.get('user_id'), genre=genre, id=movie[0], title=movie[1], poster=movie[2], url=movie[3], duration=movie[4], director=movie[5], description=movie[6] )}


def search_movies():
    # get movie titles in genres
    genres = """SELECT DISTINCT genre FROM genre"""
    genres = [g[0] for g in db.session.execute(genres).all()][:no_imdb_genres]

    movie_all = {}
    genres_query = lambda g: """SELECT DISTINCT movie_id FROM genre WHERE genre='{}'""".format(g)
    movie_query = lambda m: """SELECT DISTINCT id, title, poster_address FROM movies WHERE movies.id='{}'""".format(m)


    unique_titles = []
    for genre in genres:
        movies = [db.session.execute(movie_query(mid[0])).all() for mid in db.session.execute(genres_query(genre)).all()]
        new_movies = []
        for movie in movies:
            if movie and movie[0][0] not in unique_titles:
                unique_titles.append(movie[0][0])
                new_movie = []
                for i, m in enumerate(movie[0]):

                    if i == 2:
                        #new_movie.append(base64.b64encode(m).decode("utf-8"))
                        new_movie.append(m)
                    else:
                        new_movie.append(m)
                new_movies.append(new_movie)

        movie_all[genre.capitalize()] = new_movies[:no_of_movie_per_genre]

    return movie_all