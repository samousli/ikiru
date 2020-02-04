import traceback
from functools import partial
from werkzeug import exceptions
from app.common.extensions import jwt, httpauth
from app.common.responses import IkiruJsonResponse


def handle_generic(e):
    traceback.print_exception(type(e), e, e.__traceback__)
    if isinstance(e, exceptions.HTTPException):
        return IkiruJsonResponse(message=e.description, status_code=e.code)


def error_logger(original_handler, e):
    print(f'[DEBUG] {e.__class__}: {e}')
    return original_handler(e)


def usr_error_logger(original_handler, e):
    print(f'[DEBUG] {e.__class__}: {e}')
    # raise Exception from e
    return original_handler(e)


def register_error_handlers(app):

    # Undoing flask-restful's stupid idea of stopping exception propagation
    while isinstance(app.handle_exception, partial):
        app.handle_exception = app.handle_exception.args[0]
    while isinstance(app.handle_user_exception, partial):
        app.handle_user_exception = app.handle_user_exception.args[0]

    # Some MITM error logging in order to see the internally handled exceptions
    # if app.config['DEBUG']:
    #     app.handle_exception = partial(error_logger, app.handle_exception)
    #     app.handle_user_exception = partial(usr_error_logger, app.handle_user_exception)

    # Keeping codes as is, changing response format
    _IJR = IkiruJsonResponse

    @httpauth.error_handler
    def auth_error():
        return IkiruJsonResponse(message='Incorrect credentials.', status_code=401)

    @jwt.claims_verification_failed_loader
    def r400(msg): return _IJR(message=f'[JWT] {msg}', status_code=400)

    @jwt.unauthorized_loader
    @jwt.expired_token_loader
    @jwt.revoked_token_loader
    @jwt.needs_fresh_token_loader
    @jwt.user_loader_error_loader
    def r401(msg): return _IJR(message=f'[JWT] {msg}', status_code=401)

    @jwt.token_in_blacklist_loader
    def r403(msg): return _IJR(message=f'[JWT] {msg}', status_code=403)

    @jwt.invalid_token_loader
    def r422(msg): return _IJR(message=f'[JWT] {msg}', status_code=422)

    app.register_error_handler(Exception, handle_generic)
