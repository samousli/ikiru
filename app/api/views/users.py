from flask_restful import Resource, reqparse
from app.api import services
from app.auth import protected, AuthType
from app.common.validators import email


class UsersResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'username', dest='username',
        location='json', required=True,
        help='The username field is required.',
    )
    post_parser.add_argument(
        'email', dest='email',
        type=email, location='json',
        required=True,
        help='The email field is required.',
    )
    post_parser.add_argument(
        'password', dest='password',
        location='json', required=True,
        help='The password field is required.',
    )

    def post(self):
        return services.user.create_user(self.post_parser)


class UserResource(Resource):
    method_decorators = [protected(AuthType.JWT, self_only=True)]

    def get(self, user_uuid):
        return services.user.get_active_user()


class UserRentalsResource(Resource):
    method_decorators = [protected(AuthType.JWT, self_only=True)]

    def get(self, user_uuid):
        return services.user.get_user_rentals(user_uuid)
