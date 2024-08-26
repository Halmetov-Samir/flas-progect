import requests
from http import  HTTPStatus
ENPOIND = "http://127.0.0.1:5000"
def posts_create():
    return {
        "author_id": 0,
        "text": 'hello',
        "reactions": []
    }

def reactions():
    return {
    "user_id": "0",
    "reaction": "like",
    }

def create_users_payload():
    return {
        "first_name": "Samir",
        "last_name": "Halmetov",
        "email": "test@test.ru",
        "total_reactions":10
    }

def test_post_create():
    payload = posts_create()
    create_response = requests.post(f"{ENPOIND}/post/create",json=payload)
    assert create_response.status_code == HTTPStatus.OK
    post_data = create_response.json()
    post_id = post_data['id']

    assert post_data['author_id'] == payload['author_id']
    assert post_data['text'] == payload['text']
    assert post_data['reactions'] ==[]

    get_response = requests.get(f"{ENPOIND}/post/{post_id}",json=payload)
    assert get_response.json()['author_id'] == payload['author_id']
    assert get_response.json()['text'] == payload['text']
    assert get_response.json()['reactions'] ==[]

    payload = reactions()
    post_response = requests.post(f"{ENPOIND}/posts/{post_id}/reaction", json=payload)
    assert post_response.status_code == HTTPStatus.OK


def test_users_posts_asc():
    user_payload = create_users_payload()
    create_user_response = requests.post(f"{ENPOIND}/users/create", json=user_payload)
    assert create_user_response.status_code == HTTPStatus.OK
    user_data = create_user_response.json()
    user_id = user_data['id']

    for _ in range(3):
        post_payload = posts_create()
        create_post_response = requests.post(f"{ENPOIND}/post/create", json=post_payload)
        assert create_post_response.status_code == HTTPStatus.OK

    payload = {'sort':'asc'}

    get_response = requests.get(f"{ENPOIND}/users/{user_id}/posts", json=payload)
    assert get_response.status_code == HTTPStatus.OK
    posts = get_response.json()['posts']
    assert isinstance(posts,list)
    for i in range(len(posts) - 1):
        if all([
            'reactions' in posts[i],
            'reactions' in posts[i + 1],
            len(posts[i]['reactions']) > 0,
            len(posts[i + 1]['reactions']) > 0
        ]):
            assert len(posts[i]['reactions']) <= len(posts[i + 1]['reactions'])

def test_users_posts_desc():
    user_payload = create_users_payload()
    create_user_response = requests.post(f"{ENPOIND}/users/create", json=user_payload)
    assert create_user_response.status_code == HTTPStatus.OK
    user_data = create_user_response.json()
    user_id = user_data['id']

    for _ in range(3):
        post_payload = posts_create()
        create_post_response = requests.post(f"{ENPOIND}/post/create", json=post_payload)
        assert create_post_response.status_code == HTTPStatus.OK

    payload = {'sort':'desc'}

    get_response = requests.get(f"{ENPOIND}/users/{user_id}/posts", json=payload)
    assert get_response.status_code == HTTPStatus.OK
    posts = get_response.json()['posts']
    assert isinstance(posts,list)
    for i in range(len(posts) - 1):
        if all([
            'reactions' in posts[i],
            'reactions' in posts[i + 1],
            len(posts[i]['reactions']) > 0,
            len(posts[i + 1]['reactions']) > 0
        ]):
            assert len(posts[i]['reactions']) >= len(posts[i + 1]['reactions'])




