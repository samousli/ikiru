from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint('api', __name__)
api_v1 = Api(api_blueprint)

from .views.users import UserResource, UsersResource, UserRentalsResource
api_v1.add_resource(UsersResource, '/users')
api_v1.add_resource(UserResource, '/users/<user_uuid>')
api_v1.add_resource(UserRentalsResource, '/users/<user_uuid>/rentals')
# api_v1.add_resource(UserMovieResource, '/users/<user_uuid>/movies/<movie_uuid>')

from .views.movies import MovieResource, MoviesResource
api_v1.add_resource(MoviesResource, '/movies')
api_v1.add_resource(MovieResource, '/movies/<movie_uuid>')
# api_v1.add_resource(MovieRentalsResource, '/movies/<uuid>/rentals')

from .views.rentals import RentalsResource
api_v1.add_resource(RentalsResource, '/rentals')

from .views.genres import GenresResource, GenreMoviesResource
api_v1.add_resource(GenresResource, '/genres')
api_v1.add_resource(GenreMoviesResource, '/genres/<genre_uuid>/movies')

from .views.returns import ReturnsResource
api_v1.add_resource(ReturnsResource, '/returns')
