from flask import Blueprint, render_template
#from ..models import *

profile = Blueprint('profile', __name__)

@profile.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('profile/profile.html')