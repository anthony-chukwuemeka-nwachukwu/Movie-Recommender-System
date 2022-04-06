from flask import Blueprint, flash, redirect, render_template, request, url_for
from src import db, session
from src.models.user import User
from src.forms.login import LoginForm
from src.param import signed_in, signed_out

from src.utils.production.movie_recommder import MovieRecommender

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def login_user():

    # download files for recommender training starts
    """movieRecommender = MovieRecommender()
    movies = movieRecommender.movies_by_genres()
    users = movieRecommender.users_by_genres()
    star = movieRecommender.users_by_movies()

    import csv
    path = "/home/anthony/Documents/Strive/Movie-Recommender-System/src/utils/development/data/"

    files = ["movies", "users", "star"]
    dat = [movies, users, star]
    for i in range(len(dat)):
        with open(path+files[i]+".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(dat[i])
    print(movies.shape,users.shape,star.shape)
    print(star[0])"""
    # download files for recommender training ends


    if session.get('user'):
        return redirect(url_for('index.home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.query(User).filter(User.username == email).first()
        user_exist = user is not None

        if user_exist and user.password == password:
            flash(f'{user.first_name}, you are successfully logged in!')
            session['user'] = user.first_name.capitalize()
            session['user_id'] = user.username

            return redirect(url_for('index.home'))
        else:
            flash('Sorry, something went wrong.', 'danger')
    return render_template('login.html', title='Login', form=form)
