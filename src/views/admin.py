from flask import Blueprint, render_template
#from src.models import *

admin = Blueprint('admin', __name__)

@admin.route('/<user_url_slug>')
def timeline(user_url_slug):
    # Do some stuff
    return render_template('admin/admin.html')

