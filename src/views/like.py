import base64
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from src import db
from src.models.movies_user_like import MoviesUserLike
from src.models.user import User
from src.forms.register import RegisterForm
from src.param import signed_in, no_of_movie_per_genre, no_imdb_genres
from src.views.movie import get_movie

like = Blueprint('like', __name__)

@like.route('/like<like_id>', methods=['POST', 'GET'])
def delete_like(like_id):
    query = """DELETE FROM movies_user_like WHERE movie_id='{}';""".format(like_id)
    db.session.execute(query)
    db.session.commit()
    return liked_movies()

@like.route('/like/<movieid>/<user_name>/<source>', methods=['POST', 'GET'])
def insert_like(movieid,user_name,source):
    query = """INSERT INTO movies_user_like(movie_id, username) VALUES('{}', '{}')""".format(movieid,user_name);
    db.session.execute(query)
    db.session.commit()

    if source == 'movie':
        return get_movie()

    return liked_movies()


@like.route('/like', methods=['POST', 'GET'])
def liked_movies():
    if not session.get('user'):
        return redirect(url_for('login.login_user'))
    movies = get_movies(session.get('user_id'))
    main_movie_color = request.args.get('main_movie_color')
    return render_template('like.html', movies_by_genres=movies, star_color='orange', username=session.get('user_id'))


def get_movies(user):
    # get movie titles in genres
    genres = """SELECT DISTINCT genre FROM genre"""
    genres = [g[0] for g in db.session.execute(genres).all()][:no_imdb_genres]

    movie_all = {}
    genres_query = lambda g: """SELECT DISTINCT movie_id FROM genre WHERE genre='{}'""".format(g)
    movie_query = lambda u,m: """SELECT DISTINCT m.id, m.title, m.poster_address FROM movies_user_like ml \
        JOIN movies m ON m.id=ml.movie_id WHERE ml.username='{}' AND m.id='{}'""".format(u,m)


    unique_titles = []
    for genre in genres:
        movies = [db.session.execute(movie_query(user,g[0])).all() for g in
                  db.session.execute(genres_query(genre)).all()]
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

        if new_movies != []:
            movie_all[genre.capitalize()] = new_movies[:no_of_movie_per_genre]

    return movie_all
