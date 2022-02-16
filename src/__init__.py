from flask import Flask
from .views.admin import admin
from .views.home import home
from .views.login import login
from .views.movie import movie
from .views.profile import profile
from .views.register import register

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(movie)
app.register_blueprint(profile)
app.register_blueprint(register)