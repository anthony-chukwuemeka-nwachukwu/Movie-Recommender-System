from flask import Blueprint, render_template
from src.forms.search import SearchForm

home = Blueprint('home', __name__)

@home.route("/")
@home.route("/index")
@home.route("/home")
def index():
    form = SearchForm()
    return render_template('index.html', form=form)