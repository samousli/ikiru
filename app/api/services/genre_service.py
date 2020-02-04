from app import IkiruJsonResponse
from app.models import Genre


def get_genres():
    return IkiruJsonResponse(Genre.query.all())


def get_genre_movies(genre_uuid):
    genre = Genre.get_by_uuid(genre_uuid)
    if not genre:
        return IkiruJsonResponse(None, 'Invalid genre uuid.', 404)
    return IkiruJsonResponse(genre.movies)
