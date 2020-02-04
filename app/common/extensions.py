from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth

# despite being globally defined the db object is context aware
db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()
httpauth = HTTPBasicAuth()


def register_extensions(app):
    db.init_app(app)
    # Enable DB migrations
    migrate.init_app(app, db)
    jwt.init_app(app)
