import sys

import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import User
from .populate_db import populate_movie_table, populate_user_table
from collections import namedtuple
UserJWTHeader = namedtuple('UserJWTHeader', 'header user')


# Debug markers
def pytest_configure(config):
    sys._called_from_test = True


def pytest_unconfigure(config):
    del sys._called_from_test


@pytest.fixture(scope='session')
def app(request):
    app = create_app('test')
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture(scope='session')
def db(app):
    _db = app.extensions['sqlalchemy'].db
    print(f'\n---- POPULATING DB: {_db.engine!r}\n')

    _db.create_all()
    populate_user_table(app)
    populate_movie_table(app)
    _db.session.commit()

    yield _db

    print('\n----- DROPPING DB\n')
    _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    yield app.test_client()


@pytest.fixture(scope='function')
def session(request, db):
    session = db['session_factory']()
    print('\n----- CREATE DB SESSION\n')
    yield session
    session.rollback()
    session.close()
    print('\n----- ROLLBACK DB SESSION\n')


@pytest.fixture(scope='function')
def jwt(db):
    usr = User.query.first()
    jwt = create_access_token(usr.id)
    yield UserJWTHeader(
        header={'Authorization': f'Bearer {jwt}', 'Content-Type': 'application/json'},
        user=usr
    )
