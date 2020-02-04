from flask_restful import Resource, reqparse

from app.api import services
from app.auth import protected, AuthType


class RentalsResource(Resource):
    method_decorators = [protected(AuthType.JWT, self_only=True)]

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('user_uuid', dest='user_uuid', required=True)
    post_parser.add_argument('movie_uuid', dest='movie_uuid', required=True)

    def post(self):
        # post_parser remains editable - service layer is responsible
        # for copying the parser before doing any live edits
        return services.rental.rent_movie(self.post_parser)
