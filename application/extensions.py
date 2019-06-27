from flask_admin import Admin
from flask_jwt import JWT
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

db = MongoEngine()
login_manager = LoginManager()
admin = Admin()
jwt = JWT()
