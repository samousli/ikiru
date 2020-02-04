import csv
import datetime
from app.models import db, Movie, User, Genre, MovieGenre
from collections import namedtuple, defaultdict

_Movie = namedtuple('_Movie', ['title', 'language', 'genres', 'release_year', 'imdb_id'])


def populate_user_table(app):
    with app.app_context():
        db.session.add(User(username='sah1', password='bigsecret', email='throwaway@gmail.com'))
        db.session.add(User(username='sah2', password='hugesecret', email='throwaway2@gmail.com'))
        db.session.commit()


def populate_movie_table(app):
    movie_path = '/home/avail/workspace/ikiru/resources/movie_metadata.csv'
    # os.path.join(basedir, 'resources', 'movie_metadata.csv')
    movies = []
    with open(movie_path) as f:
        rdr = csv.reader(f)
        cols = next(rdr)
        title = cols.index('movie_title')
        language = cols.index('language')
        genres = cols.index('genres')
        movie_imdb_link = cols.index('movie_imdb_link')
        title_year = cols.index('title_year')
        for r in rdr:
            movies.append(_Movie(
                title=r[title].strip(),
                language=r[language].strip(),
                genres=[x.strip().lower() for x in r[genres].split('|')],
                release_year=r[title_year],
                imdb_id=r[movie_imdb_link].split('/')[4]
            ))

        genres = {g for m in movies for g in m.genres}

        with app.app_context():

            for g in genres:
                db.session.add(Genre(name=g))
            db.session.commit()

            cats_ii = {c.name: c.id for c in Genre.query.all()}

            mappings = defaultdict(list)
            for m in movies:
                md = m._asdict()
                del md['genres']
                db_movie = Movie(**md)
                db.session.add(db_movie)
                db.session.flush([db_movie])

                for g in m.genres:
                    mappings[cats_ii[g]].append(db_movie.id)
            db.session.commit()

            for g_id, m_ids in mappings.items():
                for m_id in m_ids:
                    db.session.add(MovieGenre(movie_id=m_id, genre_id=g_id))
            db.session.commit()
