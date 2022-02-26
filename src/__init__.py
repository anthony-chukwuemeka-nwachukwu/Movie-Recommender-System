import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.urandom(32)#os.getenv('SECRET_KEY')

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(os.getenv('POSTGRES_USER'),os.getenv('POSTGRES_PW'),\
  os.getenv('POSTGRES_URL'),os.getenv('POSTGRES_PORT'),os.getenv('POSTGRES_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from src.views.admin import admin
from src.views.home import home
from src.views.login import login
from src.views.movie import movie
from src.views.profile import profile
from src.views.register import register
from src.views.search import search

app.register_blueprint(admin)
app.register_blueprint(home)
app.register_blueprint(search)
app.register_blueprint(login)
app.register_blueprint(movie)
app.register_blueprint(profile)
app.register_blueprint(register)

#from models import genre, movie, movies_user_like, review, user
