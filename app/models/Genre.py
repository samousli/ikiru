from .Base import Base
from . import db


class Genre(Base):
    name = db.Column(db.String(32), unique=True)
    movies = db.relationship('Movie', secondary='movie_genre_xref')
