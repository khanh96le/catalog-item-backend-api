"""
Some decorators use for authenticating requests with `flask_jwt`
"""
from werkzeug.security import safe_str_cmp
from app.models.user import UserModel


def authenticate(username, password):
    # Deprecated, not use in OAuth2.0
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
