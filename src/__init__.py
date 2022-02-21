import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .views.admin import admin
from .views.home import home
from .views.login import login
from .views.movie import movie
from .views.profile import profile
from .views.register import register

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.register_blueprint(admin)
app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(movie)
app.register_blueprint(profile)
app.register_blueprint(register)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(os.getenv('POSTGRES_USER'),os.getenv('POSTGRES_PW'),os.getenv('POSTGRES_URL'),os.getenv('POSTGRES_PORT'),os.getenv('POSTGRES_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)