import os
import inspect
# from app.common.encoders import ExtendedJSONEncoder
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	@classmethod
	def as_dict(cls):
		attrs = inspect.getmembers(cls, lambda m: not inspect.isroutine(m))
		return {m[0]: m[1] for m in attrs if not m[0].startswith('_')}

	# Disables the event system which tracks db commits
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# if the seed changes in every instance
	# it will invalidate any hashed values(cookies, tokens etc) between
	# restarts or cases with multiple instances
	SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(64)
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.urandom(64)

	PAGINATION_DEFAULT_SIZE = 25

	PAYMENT_CURRENCY = ('euro', 'EUR', '€')
	# 1st day to RENTAL_BOUNDARY_BRACKETS[0] gets billed RENTAL_COST_BRACKETS[0]
	# afterwards each day costs RENTAL_COST_BRACKETS[1] units
	RENTAL_COST_BRACKETS = [1, 0.5]
	# pricing tier boundaries should always be integers
	RENTAL_PRICING_TIER_BRACKETS = [3]


class DevConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
		'sqlite:///{}'.format(os.path.join(basedir, 'dev.db'))

	DEBUG = True


class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
		'sqlite:///{}'.format(os.path.join(basedir, 'test.db'))

	DEBUG = True


config = {
	'default': Config,
	'dev': DevConfig,
	'test': TestConfig
}
