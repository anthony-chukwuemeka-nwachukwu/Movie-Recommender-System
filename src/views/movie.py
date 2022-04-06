from flask import Blueprint, request, url_for, render_template,redirect
from src import session
import src.param as pm
from src.static.py.delete_like import delete_like
from src.static.py.insert_like import insert_like
from src.utils.production.utils import Utils

movie = Blueprint('movie', __name__)

@movie.route('/movie', methods=['GET'])
def get_movie():

    if not session.get('user'):
        session['sign_in_out'] = pm.signed_in
        return redirect(url_for('login.login_user'))

    id,genre,title,description,poster,url,duration,director,main_movie_color,check_if_main_movie = request.args.get('id'),request.args.get('genre'),\
        request.args.get('title'), request.args.get('description'),request.args.get('poster'),request.args.get('url'),request.args.get('duration'),\
            request.args.get('director'), request.args.get('main_movie_color'), request.args.get('check_if_main_movie')
    check=True
    print(check_if_main_movie,main_movie_color)

    # checking and unchecking stars starts
    utils = Utils()
    if check_if_main_movie:
        movieid = request.args.get('movieid')
        main_movie_color = utils.liked_movie(movieid,session.get('user_id'))
        if main_movie_color == "white":
            insert_like(movieid,session.get('user_id'))
            main_movie_color = 'orange'
        else:
            delete_like(movieid)
            main_movie_color = 'white'


    similar_movies = utils.rank_movies(title + ' ' + description, id )
    for i,movie in enumerate(similar_movies):
        star_color_id = utils.liked_movie(movie[0],session.get('user_id'))
        similar_movies[i] = list(similar_movies[i]) + [star_color_id]
        

    return render_template( 'movie.html', genre=genre, id=id, title=title, poster=poster, url=url, duration=duration, director=director,
                            description=description , similar_movies=similar_movies, main_movie_color=main_movie_color)
