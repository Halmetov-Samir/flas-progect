from app import app, USERS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt


@app.route("/")
def index():
    return "hello world"


@app.post("/users/create")
def users_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.Validate.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if models.Validate.email_in_user(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def users_id(user_id):

    if not models.Validate.is_valid_user_id(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def users_leaderboard():
    data = request.get_json()
    type = data["type"]
    sort = data["sort"]
    users = USERS[:]

    if type == "list":
        if sort == "asc":
            users.sort(key=lambda user: user.total_reactions)
        elif sort == "desc":
            users.sort(key=lambda user: user.total_reactions, reverse=True)

        response = Response(
            json.dumps(
                {
                    "users": [
                        {
                            "id": user.id,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "total_reactions": user.total_reactions,
                        }
                        for user in users
                    ]
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response
    elif type == "graph":
        fig, ax = plt.subplots()
        people = [f"{user.id} {user.first_name} {user.last_name}" for user in users]
        user_total_reactions = [user.total_reactions for user in users]
        ax.bar(people, user_total_reactions)
        ax.set_ylabel("User total_reactions")
        ax.set_title("Users leaderboard by total_reactions")
        plt.savefig("app/static/users_leaderboard")
        return Response(
            f"""<img src="{url_for('static',filename = 'users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )

    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
