from datetime import datetime
from turtle import up
from flask_sqlalchemy import SQLAlchemy
from src import db, ma
import psycopg2
from flask_marshmallow import Marshmallow


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    star = db.Column(db.Float, nullable=True)
    title = db.Column(db.String(), nullable=True)
    review = db.Column(db.String(), nullable=True)
    createdAt = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    username = db.Column(db.String(120), db.ForeignKey('users.username'))
    movie_id = db.Column(db.String(), db.ForeignKey('movies.id'))
    
    def __init__(self, id,url,star,title,review,createdAt,updatedAt,username,movie_id):
        self.id = id
        self.url = url
        self.star = star
        self.title = title
        self.review = review
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.username = username
        self.movie_id = movie_id


class User(db.Model):
    __tablename__ = 'users'

    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(100), nullable=False)
    liked_movies= db.relationship('Movie', backref='user', lazy=True)
    reviews= db.relationship('Review', backref='user', lazy=True)

    def __init__(self, username,password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.email



class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String(), unique=False, nullable=False)
    url = db.Column(db.String(), unique=False, nullable=False)
    poster = db.Column(db.LargeBinary(), nullable=True)
    description = db.Column(db.String(), unique=False, nullable=True)
    release_date = db.Column(db.String(), nullable=True)
    duration = db.Column(db.String(), unique=False, nullable=True)
    director = db.Column(db.String(), unique=False, nullable=True)
    genries= db.relationship('Genre', backref='movie', lazy=True)
    reviews= db.relationship('Review', backref='movie', lazy=True)
    username = db.Column(db.String(120), db.ForeignKey('users.username'))

    def __init__(self, id,title,url,poster,description,release_date,duration,director):
        self.id = id
        self.title = title
        self.url = url
        self.poster = poster
        self.description = description
        self.release_date = release_date
        self.duration = duration
        self.director = director


class Genre(db.Model):
    __tablename__ = 'genres'

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64), unique=False, nullable=False)
    movie_id= db.Column(db.String(), db.ForeignKey('movies.id'))
    
    def __init__(self, name,movie_id):
        self.name = name
        self.movie_id = movie_id

# Schema
class ReviewSchema(ma.Schema):
  class Meta:
    fields = ('id','url','star','title','review','createdAt','updatedAt','username','movie_id')
class UserSchema(ma.Schema):
  class Meta:
    fields = ('username','password')
class MovieSchema(ma.Schema):
  class Meta:
    fields = ('id','title','url','poster','description','release_date','duration','director')
class GenreSchema(ma.Schema):
  class Meta:
    fields = ('name','movie_id')

# Init schema
comment_schema = ReviewSchema()
comment_schemas = ReviewSchema(many=True)

user_schema = UserSchema()
user_schemas = UserSchema(many=True)

movie_schema = MovieSchema()
movie_schemas = MovieSchema(many=True)

genre_schema = GenreSchema()
genre_schemas = GenreSchema(many=True)

def createTables():
    db.drop_all()
    db.create_all()



if __name__ == "__main__":
    createTables()