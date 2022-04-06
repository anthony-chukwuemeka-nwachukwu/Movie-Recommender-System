from flask import Blueprint, render_template
from src.forms.search import SearchForm
import src.param as pm

home = Blueprint('home', __name__)


@home.route("/")
@home.route("/index")
@home.route("/home")
def index():
    form = SearchForm()
    app_title = pm.app_title
    return render_template('index.html', form=form, app_title=app_title)
