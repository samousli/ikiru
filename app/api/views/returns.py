from flask_restful import Resource, reqparse
from app.api import services
from app.auth import protected, AuthType


class ReturnsResource(Resource):
    method_decorators = [protected(AuthType.JWT, self_only=True)]

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('rental_uuid', dest='rental_uuid', required=True)

    def post(self):
        # post_parser remains editable - service layer is responsible
        # for copying the parser before doing any live edits
        return services.rental.return_rental(self.post_parser)


class ReturnResource(Resource):
    method_decorators = [protected(AuthType.JWT, self_only=True)]

    def get(self, rental_uuid):
        return services.rental.get_cost(rental_uuid)