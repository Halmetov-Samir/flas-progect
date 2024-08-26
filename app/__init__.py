from flask import Flask

USERS = []
POSTS = []
app = Flask(__name__)
from app import views
from app import tests
