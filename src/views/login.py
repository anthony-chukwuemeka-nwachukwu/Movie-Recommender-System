from flask import Blueprint, render_template
from ..models import *

login = Blueprint('login', __name__)

@login.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('login/login.html')