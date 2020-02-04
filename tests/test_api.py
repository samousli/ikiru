from app.models import User, Movie, Rental


def test_create_users(client, jwt):

    # ToDo: Get rid of flask-restful....it doesn't allow us to handle our own errors for RequestParser
    response = client.post(
        '/api/v1/users',
        headers=jwt.header,
        json={'username': 'sah3', 'password': 'mongosecret'}
    )
    assert response.status_code == 400

    response = client.post(
        '/api/v1/users',
        headers=jwt.header,
        json={'username': 'sah3', 'password': 'mongosecret', 'email': 'nope@nope2.com'}
    )
    assert response.status_code == 200


def test_rent_movie(client, db, jwt):

    movie = Movie.query.first()

    response = client.post(
        '/api/v1/rentals',
        headers=jwt.header,
        json={'user_uuid': jwt.user.uuid, 'movie_uuid': movie.uuid}
    )
    assert response.status_code == 200

    rental = Rental.query.filter_by(movie_id=movie.id, user_id=jwt.user.id).one_or_none()
    # print(rental.as_dict(ignore_list=[]))
    assert rental


def test_forbidden_rent_movie(client, db, jwt):

    movie = Movie.query.first()
    user = User.query.filter(User.id!=jwt.user.id).first()
    response = client.post(
        '/api/v1/rentals',
        headers=jwt.header,
        json={'user_uuid': user.uuid, 'movie_uuid': movie.uuid}
    )
    print(response.get_json())
    assert response.status_code == 403


def test_forbidden_rent_movie(client, db, jwt):

    movie = Movie.query.first()
    user = User.query.filter(User.id!=jwt.user.id).first()
    response = client.post(
        '/api/v1/rentals',
        headers=jwt.header,
        json={'user_uuid': user.uuid, 'movie_uuid': movie.uuid}
    )
    print(response.get_json())
    assert response.status_code == 403