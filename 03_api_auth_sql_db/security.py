from user import User
from werkzeug.security import safe_str_cmp # safer way to compare string

users = [
    User(1, 'bob', 'asdf')
]


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_userid(user_id)