import base64
from flask import Blueprint, render_template, redirect, request, url_for
from src import session, db
from src.forms.search import SearchForm
import src.param as pm
from src.static.py.delete_like import delete_like
from src.static.py.insert_like import insert_like
from src.utils.production.utils import Utils

index = Blueprint('index', __name__)


@index.route("/", methods=['POST', 'GET'])
@index.route("/index", methods=['POST', 'GET'])
@index.route("/home", methods=['POST', 'GET'])
def home():
    form = SearchForm()
    app_title = pm.app_title
    if not session.get('user'):
        session['sign_in_out'] = pm.signed_in
        return redirect(url_for('login.login_user'))

    utils = Utils()
    query = request.args.get('query')

    if request.method == 'POST':
        session['search_query'] = form.query.data
        genres, sorted_keys = utils.search_movies(session['search_query'])
    else:
        if query == 'True':
            try:
                genres, sorted_keys = utils.search_movies(session['search_query'])
            except:
                genres, sorted_keys = utils.get_movies()
        else:
            genres, sorted_keys = utils.get_movies()

    # checking and unchecking start starts
    movieid = request.args.get('id')
    star_color = utils.liked_movie(movieid, session.get('user_id'))
    if star_color == "white":
        insert_like(movieid, session.get('user_id'))
    else:
        delete_like(movieid)
    # star_color = utils.liked_movie(movieid,session.get('user_id'))

    for genre in genres:
        for i, movie in enumerate(genres[genre]):
            genres[genre][i] = list(genres[genre][i]) + [utils.liked_movie(movie[0], session.get('user_id'))]

    session['sign_in_out'] = pm.signed_out
    return render_template('index.html', genres=genres, sorted_keys=sorted_keys, form=form, app_title=app_title,
                           signed_in=pm.signed_in)
