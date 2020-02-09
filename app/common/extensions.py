from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth


# despite being globally defined the db object is context aware
db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()
httpauth = HTTPBasicAuth()


def register_db(app):
    db.init_app(app)
    # Enable DB migrations
    migrate.init_app(app, db)


def register_extensions(app):
    jwt.init_app(app)


def setup_db_config(app, config_name):
    from app.models import Config
    with app.app_context():
        # Database not initialized yet
        if not db.engine.has_table(Config.__tablename__):
            return

        if Config.query.count() == 0:
            from config import config
            Config.populate_from_conf_object(config[config_name], config_name)
        else:
            Config.load_from_db(app)
