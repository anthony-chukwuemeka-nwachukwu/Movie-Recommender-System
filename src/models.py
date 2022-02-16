from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.email'))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'users'

    email= db.Column(db.String(120), primary_key=True)
    username= db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(100), nullable=False)
    liked_movies= db.relationship('Movie', backref='user', lazy=True)
    comments= db.relationship('Comment', backref='user', lazy=True)

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

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(), unique=False, nullable=False)
    description= db.Column(db.String(), unique=False, nullable=True)
    link= db.Column(db.String(), unique=False, nullable=False)
    poster= db.Column(db.String(), unique=False, nullable=True)
    genries= db.relationship('Genre', backref='movie', lazy=True)
    comments= db.relationship('Comment', backref='movie', lazy=True)
    user_id = db.Column(db.String(120), db.ForeignKey('users.email'))


class Genre(db.Model):
    __tablename__ = 'genres'

    id= db.Column(db.Integer, primary_key=True, unique=True)
    name= db.Column(db.String(64), unique=False, nullable=False)
    movie_id= db.Column(db.Integer, db.ForeignKey('movies.id'))

