from flask import Blueprint, render_template
#from ..models import *

home = Blueprint('home', __name__)

@home.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('home/home.html')