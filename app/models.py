import re
from app import USERS, POSTS


class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    def add_posts(self, post):
        self.posts.append(post)
        POSTS.append(post)

    def __lt__(self, other):
        return self.total_reactions < other.total_reactions


class Posts:
    def __init__(self, id, author_id, text):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    def add_reactions(self, reaction):
        self.reactions.append(reaction)
        USERS[self.author_id].total_reactions += 1
        self.sort_reaction()

    def sort_reaction(self):
        self.reactions = sorted(self.reactions)


# todo:finish is the class Validate
class Validate:
    @staticmethod
    def is_valid_reaction(reaction):
        reactions = ["heart", "like", "dislike", "boom", "joker"]
        return reaction in reactions

    @staticmethod
    def is_valid_user_id(user_id):
        return 0 <= user_id < len(USERS)

    @staticmethod
    def is_valid_post_id(post_id):
        return 0 <= post_id < len(POSTS)

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    staticmethod

    def email_in_user(email):
        return any(user.email == email for user in USERS)
