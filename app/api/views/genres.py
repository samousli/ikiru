from flask_restful import Resource

from app.api import services
from app.auth import protected, AuthType


class GenresResource(Resource):
    method_decorators = [protected(AuthType.JWT)]

    def get(self):
        return services.genre.get_genres()


class GenreMoviesResource(Resource):
    method_decorators = [protected(AuthType.JWT)]

    def get(self, genre_uuid):
        return services.genre.get_genre_movies(genre_uuid)
