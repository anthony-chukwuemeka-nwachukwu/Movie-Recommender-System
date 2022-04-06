import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from flask_marshmallow import Marshmallow
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)  # os.getenv('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config["CACHE_TYPE"] = "null"
app.config["SESSION_TYPE"] = "null"
#basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(os.getenv('POSTGRES_USER'),
                                                                             os.getenv('POSTGRES_PW'),
                                                                             os.getenv('POSTGRES_URL'),
                                                                             os.getenv('POSTGRES_PORT'),
                                                                             os.getenv('POSTGRES_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Session(app)
session = session

db = SQLAlchemy(app)
ma = Marshmallow(app)

from src.views.admin import admin
from src.views.index import index
from src.views.login import login
from src.views.logout import logout
from src.views.movie import movie
from src.views.profile import profile
from src.views.register import register
from src.views.like import like
#from src.views.search import search


app.register_blueprint(admin)
app.register_blueprint(index)
#app.register_blueprint(search)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(movie)
app.register_blueprint(profile)
app.register_blueprint(register)
app.register_blueprint(like)

