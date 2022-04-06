from flask import Blueprint, render_template
#from src.models import *
from src import db

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET'])
def timeline():
    genres = """SELECT DISTINCT genre FROM genre"""
    genres = [g[0] for g in db.session.execute(genres).all()]
    genres = """SELECT DISTINCT movie_id FROM genre WHERE genre='{}'""".format(genres[0])
    genres = [g[0] for g in db.session.execute(genres).all()[:5]]
    print(genres)
    return "render_template('admin/admin.html')"

if __name__ == '__main__':
    timeline()

