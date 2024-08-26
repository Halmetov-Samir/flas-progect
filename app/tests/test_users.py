import requests
from http import HTTPStatus
from uuid import uuid4
import os

ENPOIND = "http://127.0.0.1:5000"
def create_users_payload():
    return {
        "first_name": "Samir",
        "last_name": "Halmetov",
        "email": "test@test.ru",
        "total_reactions":10
    }


def test_users_create():
    payload = create_users_payload()
    create_response = requests.post(f"{ENPOIND}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]

    get_response = requests.get(f"{ENPOIND}/users/{user_id}", json=payload)
    assert get_response.json()['first_name'] == payload['first_name']
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]



def test_valid_email():
    payload = create_users_payload()
    payload["email"] = 'test_test.ru'
    create_response = requests.post(f"{ENPOIND}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST

def test_users_leaderboard_list_asc():
    for _ in range(3):
        payload = create_users_payload()
        create_response = requests.post(f"{ENPOIND}/users/create",json=payload)
        assert create_response.status_code == HTTPStatus.OK

    payload = {'type':'list','sort':'asc'}
    get_response = requests.get(f"{ENPOIND}/users/leaderboard",json=payload)
    users = get_response.json()['users']
    assert isinstance(users,list)
    assert users[0]['total_reactions'] <= users[1]['total_reactions']
    assert users[1]['total_reactions'] <= users[2]['total_reactions']

def test_users_leaderboard_list_desk():
    for _ in range(3):
        payload = create_users_payload()
        create_response = requests.post(f"{ENPOIND}/users/create",json=payload)
        assert create_response.status_code == HTTPStatus.OK

    payload = {'type':'list','sort':'desk'}
    get_response = requests.get(f"{ENPOIND}/users/leaderboard",json=payload)
    users = get_response.json()['users']
    assert isinstance(users,list)
    assert users[0]['total_reactions'] >= users[1]['total_reactions']
    assert users[1]['total_reactions'] >= users[2]['total_reactions']


def test_users_leaderboard_graph():
    for _ in range(3):
        payload = create_users_payload()
        create_response = requests.post(f"{ENPOIND}/users/create",json=payload)
        assert create_response.status_code == HTTPStatus.OK
    payload = {'type': 'graph'}
    get_response = requests.get(f"{ENPOIND}/users/leaderboard", json=payload)
    assert get_response.headers['Content-Type'] == 'text/html; charset=utf-8'





