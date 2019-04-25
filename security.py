from werkzeug.security import safe_str_cmp
from models.user import UserModel
from functools import wraps
from flask_restful import abort

def authenticate(username, password):
    user = UserModel.find(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)


if __name__ == "__main__":
    pass