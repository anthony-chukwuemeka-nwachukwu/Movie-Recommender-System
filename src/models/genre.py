from src import db, ma

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(64), unique=False, nullable=False)
    movie_id= db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self,genre,movie_id):
        self.genre = genre
        self.movie_id = movie_id


class GenreSchema(ma.Schema):
  class Meta:
    fields = ('id','genre','movie_id')


genre_schema = GenreSchema()
genre_schemas = GenreSchema(many=True)