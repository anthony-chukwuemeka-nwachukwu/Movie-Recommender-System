from flask import Blueprint, jsonify, render_template
from src import db
from src.models.movie import Movie, movie_schemas

movie = Blueprint('movie', __name__)

@movie.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):

    """try:
        movieId = db.session.query(Movie).filter(Movie.id == movie_id).first()
        return movie_schema.dump(movieId)#render_template('movie.html')
    except:
        return {'Error':'invalid movie'}"""
    movieId = db.session.query(Movie).filter(Movie.id == movie_id).first_or_404()
    print(movieId.genres_movie_belongs_to)
    return movie_schemas.dump(movieId.genres_movie_belongs_to)#movie_schema.dump(movieId)#render_template('movie.html')

