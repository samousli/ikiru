import datetime

from flask import current_app
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from app.models import db, Movie
from app.common.responses import IkiruJsonResponse, Status


def create_movie(parser):
    args = parser.parse_args()
    args['release_date'] = datetime.datetime(year=args['release_date'], month=1, day=1)

    movie = Movie(**args)
    db.session.add(movie)
    try:
        db.session.commit()
    except IntegrityError as e:
        return IkiruJsonResponse(None, 'Movie already exists.', Status.CONFLICT)

    db.session.refresh(movie)
    return IkiruJsonResponse(movie, 'Movie created successfully.')


get_movies_parser = reqparse.RequestParser()
get_movies_parser.add_argument('page', dest='page', type=int, default=1)
get_movies_parser.add_argument('page_size', type=int, dest='page_size')


def get_movie_by_uuid(uuid):
    movie = Movie.get_by_uuid(uuid)
    if movie is None:
        return IkiruJsonResponse(message='Movie does not exist.', status_code=404)
    m = movie.as_dict()
    m['genres'] = [g.name for g in movie.genres]
    return IkiruJsonResponse(m)


def get_movies():
    args = get_movies_parser.parse_args()
    page = args.get('page')
    page_size = args.get('page_size', None)
    if not page_size:
        app = current_app._get_current_object()
        page_size = page_size or app.config.get('PAGINATION_DEFAULT_SIZE', None) or 100
    return IkiruJsonResponse(payload=Movie.query.paginate(page, page_size, False).items)


def get_movie_rentals(uuid):
    movie = Movie.get_by_uuid(uuid)
    if movie is None:
        return IkiruJsonResponse(message='Movie does not exist.', status_code=404)
    return IkiruJsonResponse(movie.rentals)
