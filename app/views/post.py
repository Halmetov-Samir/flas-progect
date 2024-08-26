from app import app, USERS, models,POSTS
from flask import request, Response
import json
from http import HTTPStatus

@app.post("/post/create")
def post_create():
    data = request.get_json()
    id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]

    if author_id < 0 or author_id > len(USERS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = models.Posts(id, author_id, text)
    USERS[author_id].add_posts(post)

    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response

@app.get("/post/<int:post_id>")
def posts_id(post_id):
    if not models.Validate.is_valid_post_id(post_id):
        return Response(status=HTTPStatus.NOT_FOUND)

    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response

@app.post("/posts/<int:post_id>/reaction")
def post_reactions(post_id):
    data = request.get_json()
    user_id = data.get("user_id")
    reaction = data.get("reaction")

    if not models.Validate.is_valid_post_id(post_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    if not models.Validate.is_valid_reaction(reaction):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = POSTS[post_id]
    post.add_reactions(reaction)

    return Response(status=HTTPStatus.OK)

@app.get("/users/<int:user_id>/posts")
def users_posts(user_id):
    data = request.get_json()
    sort = data["sort"]

    if not models.Validate.is_valid_user_id:
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    posts = user.posts

    if sort == "asc":
        posts.sort(key=lambda post: len(post.reactions))
    elif sort == "desc":
        posts.sort(key=lambda post: len(post.reactions), reverse=True)

    response = Response(
        json.dumps(
            {
                "posts": [
                    {
                        "id": post.id,
                        "author_id": post.author_id,
                        "text": post.text,
                        "reactions": post.reactions,
                    }
                    for post in posts
                ]
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
