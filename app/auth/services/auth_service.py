import enum
import functools

from flask import g
from flask import request
from flask_restful import abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User
from app.common.extensions import httpauth

USER_UUID_FIELD_NAME = 'user_uuid'


class AuthType(enum.IntEnum):
    Simple = 1
    JWT = 2


@httpauth.verify_password
def verify_password(username, password):
    g.user = User.query.filter_by(username=username).one_or_none()
    return g.user is not None and g.user.verify_password(password)


def __get_jwt_user_if_exists():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def protected(auth_method=None, self_only=False):
    """
    Decorated function requires authentication
    @param auth_method: viable authentication methods selected from AuthType enum
    @param self_only: used to restrict access to owned resources only, wherever applicable
    """
    argless_call = callable(auth_method)
    func = auth_method
    if argless_call or auth_method is None:
        auth_method = AuthType.Simple

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal f

            # called in reverse order, self_only after auth steps
            if self_only:
                f = __self_only(f)

            f = __load_user_to_g(f)

            if auth_method is AuthType.JWT:
                f = jwt_required(f)
            elif auth_method is AuthType.Simple:
                f = httpauth.login_required(f)

            return f(*args, **kwargs)

        return wrapper
    if argless_call:
        return decorator(func)
    return decorator


def __load_user_to_g(func):
    """
    `me` keyword as a unique user identifier.... e.g /users/me/rentals
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_uuid = kwargs.get(USER_UUID_FIELD_NAME, None)
        if user_uuid is None or user_uuid == 'me':
            g.user = g.user or __get_jwt_user_if_exists()
        else:
            usr = User.get_by_uuid(user_uuid)
            if usr:
                g.user = usr
            else:
                abort(404)

        return func(*args, **kwargs)
    return wrapper


def __self_only(func):
    """
    Used to restrict access to owned resources only
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # check if user credentials passed through kwargs belong to user

        uuid = kwargs.get(USER_UUID_FIELD_NAME, None)
        if not uuid:
            json = request.get_json()
            uuid = json and json.get(USER_UUID_FIELD_NAME, None)

        if uuid and uuid == 'me':
            return func(*args, **kwargs)

        # if not uuid and request.data:
        #     raise ValueError('Data to be parsed exists.')

        if uuid and g.user.uuid != uuid:
            abort(403)
        return func(*args, **kwargs)
    return wrapper
