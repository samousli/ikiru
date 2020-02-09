from werkzeug.security import generate_password_hash, check_password_hash

from . import Base
from . import db


class User(Base):

	username = db.Column(db.String(64), unique=True, nullable=False)
	_password_hash = db.Column(db.String(256), nullable=False)
	# first_name = db.Column(db.String(64), nullable=False)
	# last_name = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(64), nullable=False)

	rentals = db.relationship('Rental', back_populates='user', lazy=True)

	@property
	def password(self):
		raise AttributeError('password field not accessible')

	@password.setter
	def password(self, password):
		# PBKDF2 with sys_rng 8 char salt and 150000 iterations
		self._password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self._password_hash, password)

	def get_active_rentals(self):
		return (r for r in self.rentals if not r.was_returned())

	def get_past_rentals(self):
		return (r for r in self.rentals if r.was_returned())
