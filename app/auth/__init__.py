"""
All things related to authentication code go in here
"""
from flask import Blueprint
from flask_restful import Api

from .services.auth_service import protected, AuthType

auth_blueprint = Blueprint('auth', __name__)
auth_api = Api(auth_blueprint)

from .views.token import TokenResource, EvalResource
auth_api.add_resource(TokenResource, '/token')
auth_api.add_resource(EvalResource, '/eval')
