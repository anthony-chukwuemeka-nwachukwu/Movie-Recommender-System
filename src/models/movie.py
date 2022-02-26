from src import db, ma

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.String(120), primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(), unique=False, nullable=False)
    poster = db.Column(db.LargeBinary(), nullable=True)
    description = db.Column(db.String(), unique=False, nullable=True)
    release_date = db.Column(db.String(120), nullable=True)
    duration = db.Column(db.String(120), unique=False, nullable=True)
    director = db.Column(db.String(120), unique=False, nullable=True)

    def __init__(self,id,title,url,poster,description,release_date,duration,director):
        self.id = id
        self.title = title
        self.url = url
        self.poster = poster
        self.description = description
        self.release_date = release_date
        self.duration = duration
        self.director = director


class MovieSchema(ma.Schema):
  class Meta:
    fields = ('id','title','url','poster','description','release_date','duration','director')

movie_schema = MovieSchema()
movie_schemas = MovieSchema(many=True)