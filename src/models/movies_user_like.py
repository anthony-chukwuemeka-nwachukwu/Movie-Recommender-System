from src import db, ma

class MoviesUserLike(db.Model):
    __tablename__ = 'movies_user_like'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(120), unique=False)
    username= db.Column(db.String(120), unique=False)

    def __init__(self,username,movie_id):
        self.username = username
        self.movie_id = movie_id


class MoviesUserLikeSchema(ma.Schema):
  class Meta:
    fields = ('id','username','movie_id')

movies_user_like_schema = MoviesUserLikeSchema()
movies_user_like_schemas = MoviesUserLikeSchema(many=True)