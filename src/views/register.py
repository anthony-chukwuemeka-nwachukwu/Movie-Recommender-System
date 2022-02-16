from flask import Blueprint, render_template
from ..models import *

register = Blueprint('register', __name__)

@register.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('register/register.html')