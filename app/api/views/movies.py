from flask_restful import Resource

from app.api import services
from app.auth import protected, AuthType


class MoviesResource(Resource):
    method_decorators = [protected(AuthType.JWT)]

    def get(self):
        return services.movie.get_movies()

    # post_parser = reqparse.RequestParser()
    # post_parser.add_argument(
    #     'title', dest='title', required=True,
    #     help='title field is required.'
    # )
    # post_parser.add_argument(
    #     'language', dest='language', required=True,
    #     help='language field is required.'
    # )
    # post_parser.add_argument(
    #     'imdb_id', dest='imdb_id',
    #     help='password field is required.'
    # )
    # post_parser.add_argument(
    #     'release_year', dest='release_date', type=int, required=True,
    #     help='release_date field is required.'
    # )
    # def post(self):
    #     return services.movie.create_movie(self.post_parser)


class MovieResource(Resource):
    method_decorators = [protected(AuthType.JWT)]

    def get(self, movie_uuid):
        return services.movie.get_movie_by_uuid(movie_uuid)


# not meant to be user visible
# class MovieRentalsResource(Resource):
#     method_decorators = [protected(AuthType.JWT)]
#
#     def get(self, uuid):
#         return services.movie.get_movie_rentals(uuid)
