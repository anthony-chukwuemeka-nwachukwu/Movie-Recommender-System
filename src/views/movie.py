from flask import Blueprint, render_template
from ..models import *

movie = Blueprint('movie', __name__)

@movie.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('movie/movie.html')