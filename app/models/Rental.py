from datetime import datetime
from .Base import Base
from . import db


class Rental(Base):
    _ignored_fields = Base._ignored_fields + ['user_id', 'movie_id']

    user_id = db.Column(db.ForeignKey('users.id'))
    movie_id = db.Column(db.ForeignKey('movies.id'))
    date_rented = db.Column(db.DateTime, default=datetime.utcnow())
    date_returned = db.Column(db.DateTime, default=None)

    user = db.relationship('User', back_populates='rentals', lazy=True)
    movie = db.relationship('Movie', back_populates='rentals', lazy=True)

    def was_returned(self):
        return self.date_returned is not None
