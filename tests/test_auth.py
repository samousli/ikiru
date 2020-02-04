from requests.auth import _basic_auth_str


def get_basic_auth_headers(username, password):
    return {'Authorization': _basic_auth_str(username, password)}


def get_jwt_headers(jwt):
    return {'Authorization': f'Bearer {jwt}', 'Content-Type': 'application/json'}


def test_index(app):
    from pprint import pprint
    pprint([r for r in app.url_map.iter_rules()])


def test_404(client):
    response = client.get('/wrong/url', headers=get_basic_auth_headers('email', 'password'))
    assert response.status_code == 404
    # json_response = json.loads(response.get_data(as_text=True))


def test_no_auth(client):
    response = client.get('/api/v1/users/me')
    assert response.status_code == 401


def test_bad_auth(client, db):
    response = client.post('/auth/token', headers=get_basic_auth_headers('Sah', 'badpass'))
    assert response.status_code == 401


def test_simple_auth(client, db):
    response = client.post('/auth/token', headers=get_basic_auth_headers('sah1', 'bigsecret'))
    assert response.status_code == 200

    response = client.post('/auth/token', headers=get_basic_auth_headers('sah2', 'hugesecret'))
    assert response.status_code == 200

    data = response.get_json().get('data', None)
    assert data
    token = data.get('token', None)
    assert token


def test_jwt_auth(client, db):
    response = client.post('/auth/token', headers=get_basic_auth_headers('sah1', 'bigsecret'))
    token = response.get_json()['data']['token']

    response = client.post('/auth/eval', headers=get_jwt_headers(token))
    assert response.status_code == 200
