

from .Base import Base
from . import db


class Movie(Base):
    title = db.Column(db.String(256),  nullable=False)
    language = db.Column(db.String(8), default='en')
    imdb_id = db.Column(db.String(10))
    release_year = db.Column(db.Integer)

    rentals = db.relationship('Rental', back_populates='movie', lazy=True)
    genres = db.relationship('Genre', secondary='movie_genre_xref')
