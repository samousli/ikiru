import sys

import pytest
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import User
from .populate_db import populate_movie_table, populate_user_table
from collections import namedtuple

Session = sessionmaker()
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

    _db.drop_all()
    _db.create_all()
    populate_user_table(app)
    populate_movie_table(app)
    _db.session.commit()
    try:
        yield _db
    finally:
        print('\n----- DROPPING DB\n')
        _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture(scope='function')
def session(db):
    print('\n----- CREATE DB SESSION\n')
    connection = db.engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
    print('\n----- ROLLBACK DB SESSION\n')


@pytest.fixture(scope='function')
def jwt(db):
    usr = User.query.first()
    jwt = create_access_token(usr.id)
    yield UserJWTHeader(
        header={'Authorization': f'Bearer {jwt}', 'Content-Type': 'application/json'},
        user=usr
    )
