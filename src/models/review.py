from datetime import datetime
from src import db, ma

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Float, nullable=True)
    title = db.Column(db.String(120), nullable=True)
    review = db.Column(db.String(), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    reviewer_username = db.Column(db.String(120), nullable=False, unique=False)
    movie_id = db.Column(db.String(120), nullable=False, unique=False)
    
    def __init__(self,star,title,review,createdAt,updatedAt,reviewer_username,movie_id):
        self.star = star
        self.title = title
        self.review = review
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.reviewer_username = reviewer_username
        self.movie_id = movie_id


class ReviewSchema(ma.Schema):
  class Meta:
    fields = ('id','star','title','review','createdAt','updatedAt','reviewer_username','movie_id')

review_schema = ReviewSchema()
review_schemas = ReviewSchema(many=True)