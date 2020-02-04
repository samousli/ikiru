import os
from dotenv import load_dotenv
from app import create_app

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

from flask_migrate import migrate, upgrade
from app import models
from tests.populate_db import populate_user_table, populate_movie_table


@app.shell_context_processor
def make_shell_context():
    return dict(db=models.db, models=models)


@app.cli.command()
def deploy():
    migrate()
    upgrade()
    populate_user_table(app)
    populate_movie_table(app)
