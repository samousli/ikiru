import sqlalchemy
from flask import g

from app.models import db, User
from app.common.responses import IkiruJsonResponse, Status


def create_user(parser):
    args = parser.parse_args()
    user = User(**args)
    db.session.add(user)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return IkiruJsonResponse(None, 'Username already exists.', Status.CONFLICT)

    db.session.refresh(user)
    return IkiruJsonResponse(user, 'User created successfully.')


def get_active_user():
    user = g.user
    if user is None:
        return IkiruJsonResponse(message='User does not exist.', status_code=404)
    return IkiruJsonResponse(user)


def get_user_by_uuid(uuid):
    user = g.user or User.get_by_uuid(uuid)
    if user is None:
        return IkiruJsonResponse(message='User does not exist.', status_code=404)
    return IkiruJsonResponse(user)


def get_user_rentals(uuid):
    user = g.user or User.get_by_uuid(uuid)
    if user is None:
        return IkiruJsonResponse(message='User does not exist.', status_code=404)
    return IkiruJsonResponse({
        'active_rentals': user.get_active_rentals(),
        'past_rentals': user.get_past_rentals()
    })
