from datetime import datetime

from flask import g
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_raw_jwt

from app.auth import protected, AuthType
from app.common.responses import IkiruJsonResponse


class TokenResource(Resource):
    method_decorators = [protected(AuthType.Simple, False)]

    def post(self):
        """Get bearer token via simple auth."""
        payload = {
            'user': g.user,
            'token': create_access_token(g.user.id)
        }
        return IkiruJsonResponse(payload, 'Access token created successfully.')


class EvalResource(Resource):
    method_decorators = [protected(AuthType.JWT, False)]

    def post(self):
        """ Check token validity."""
        jwt = get_raw_jwt()
        return IkiruJsonResponse({
            'user': g.user,
            'date_expires': datetime.utcfromtimestamp(jwt['exp'])
        })
