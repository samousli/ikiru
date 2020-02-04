import os
import urllib

from flask import Flask, g, url_for, current_app

from config import config
from app.common.responses import IkiruJsonResponse
from app.common.extensions import register_extensions
from app.common.error_handlers import register_error_handlers


def create_app(config_name=None):
	if not config_name:
		config_name = os.getenv('FLASK_CONFIG') or 'default'

	app = Flask(__name__)

	# clear the automatically added route for static
	app.url_map._rules.clear()
	app.url_map._rules_by_endpoint.clear()

	# load config
	app.config.from_object(config[config_name])

	register_extensions(app)
	register_blueprints(app)
	register_error_handlers(app)

	@app.before_request
	def before_request():
		g.user = None

	return app


def register_blueprints(app):
	from .auth import auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .api import api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/v1')

	app.add_url_rule('/index', 'index', site_index)


def site_index():
	output = []
	for rule in current_app.url_map.iter_rules():
		options = {}
		for arg in rule.arguments:
			options[arg] = "[{0}]".format(arg)

		url = urllib.parse.unquote(url_for(rule.endpoint, **options))
		for method in rule.methods:
			# ToDo: Dynamically insert docstrings from the endpoints
			output.append(f'{method} {url}')  # = repr(rule)
	return IkiruJsonResponse(sorted(output))

