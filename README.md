# Ikiru - Movie Rental Rest API
Built with __*Flask / SQLAlchemy / PyTest*__
and the intent to create an structure which can potentially support a large codebase.


## Endpoints
#### Public
* GET /index
* POST /api/v1/users
#### Basic auth
* POST /auth/token
#### JWT
* GET /api/v1/genres
* GET /api/v1/genres/[genre_uuid]/movies
* GET /api/v1/movies?page=1&page_size=100
* GET /api/v1/movies/[movie_uuid]
* GET /api/v1/users/[user_uuid]
* GET /api/v1/users/[user_uuid]/rentals
* POST /api/v1/rentals
* POST /api/v1/returns
* POST /auth/eval

### Future ideas:
* Get rid of flask-restful
* Add dynamic descriptions to /index via docstrings
* Add logger
* Add dynamic role/permission system
* Increase test coverage and automate the process
* Implement two-factor registration via email
* Support form-data in addition to json
* Set up proper pagination
* Integrate [marshmallow](https://marshmallow.readthedocs.io/en/stable/)


## Sample .env
```shell script
export PYTHONDONTWRITEBYTECODE='^_^'
export FLASK_ENV=ikiru
export FLASK_APP="app:create_app('dev')"
export FLASK_DEBUG=1
export SECRET_KEY='cf127eb28cf1943032adf8539813e44bfe51fdfe494d9461ae1afbaeac01803bd3d70176d23168c4fbc89525857574d17a9139b7cbc089d29ae3b3dc00e0c30c'
export JWT_SECRET_KEY='f7febd26ab81c1cc372a103d231ed7b5427d7be4ad723498914ac54c95c7bcb49a41ee97d2cbd5b5c9a8757f2305d99c786624472bfb56a8f654ef15285fd6e3'
```