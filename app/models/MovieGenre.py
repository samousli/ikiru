from . import db


# ToDo: Abstract away the association table creation code
class MovieGenre(db.Model):
    __tablename__ = 'movie_genre_xref'
    movie_id = db.Column(db.ForeignKey('movies.id'), primary_key=True)
    genre_id = db.Column(db.ForeignKey('genres.id'), primary_key=True)
