import base64
from flask import Blueprint, flash, redirect, render_template, session, url_for
from src import db
from src.models.movies_user_like import MoviesUserLike
from src.models.user import User
from src.forms.register import RegisterForm
from src.param import signed_in, no_of_movie_per_genre, min_required_no_of_movies_by_user, no_imdb_genres

register = Blueprint('register', __name__)


@register.route('/register', methods=['POST', 'GET'])
def register_user():
    movies = get_movies()
    columns = ['id', 'title', 'url', 'poster_address', 'description', 'release_date', 'duration', 'director']

    if session.get('user'):
        return redirect(url_for('index.home'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        stared_valid = form.stared_valid.data
        stared_ids = [i for i in str(form.stared_ids.data).split(',') if not i.isdigit()]

        for m_id in stared_ids:
            moviesUserLike = MoviesUserLike(username=email, movie_id=m_id)
            db.session.add(moviesUserLike)

        user = User(username=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        #add_user_dislikes(movies, email)

        flash('You are successfully registered!', 'success')
        session['user'] = None
        session['sign_in_out'] = signed_in
        return redirect(url_for('login.login_user'))

    return render_template('register.html', title='Register', form=form, movies_by_genres=movies,
                           min_required_no_of_movies_by_user=min_required_no_of_movies_by_user, no_imdb_genres=no_imdb_genres)

def add_user_dislikes(movies, username):

    likes_query = """SELECT movie_id FROM movies_user_like WHERE username = '{}'""".format(username)
    query_dislike = lambda movieid: """INSERT INTO movies_user_dislike(movie_id, username) VALUES('{}', '{}')""".format(movieid,username);
    user_likes = [l[0] for l in db.session.execute( likes_query ).all()]
    
    like_dislikes = []
    for movie in list(movies.keys()):
        like_dislikes.extend([m[0] for m in movies[movie]])
    distinct_movies = list(set(like_dislikes))
    
    for m in distinct_movies:
        if m != 'not-validated' and m not in user_likes:
            db.session.execute(query_dislike(m))
    db.session.commit()

def get_movies():
    # get movie titles in genres
    genres = """SELECT DISTINCT genre FROM genre"""
    genres = [g[0] for g in db.session.execute(genres).all()][:no_imdb_genres]

    movie_all = {}
    genres_query = lambda g: """SELECT DISTINCT movie_id FROM genre WHERE genre='{}'""".format(g)
    movie_query = lambda m: """SELECT id, title, poster_address FROM movies WHERE id='{}'""".format(m)

    # img = movies['family'][2][2]
    # image = base64.b64encode(img).decode("utf-8")

    unique_titles = []
    for genre in genres:
        movies = [db.session.execute(movie_query(g[0])).all() for g in
                  db.session.execute(genres_query(genre)).all()]
        new_movies = []
        items = []#doing nothing
        for movie in movies:
            items.append(movie[0][0])#doing nothing
            if movie[0][0] not in unique_titles:
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
