import sqlite3
from flask_restful import Resource
from flask_restful import reqparse
from models.user import UserModel

def none_empty_string(s):
        if not s:
            raise ValueError("Must not be an empty string")
        if not isinstance(s, str):
            raise ValueError("Must be of type string")
        return s

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=none_empty_string,
        required=True,
        nullable=False
    )
    parser.add_argument('password',
        type=none_empty_string,
        required=True,
        nullable=False
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        #check for user uniqueness
        name = data['username']
        user = UserModel.find(name)
        print('User found is ')
        print(user)
        if user:
            return {'message': "A user with the username {} already exists".format(name)}, 400
        # conn = sqlite3.connect('data.db')
        # cursor = conn.cursor()

        # query = "INSERT INTO users VALUES (NULL, ?, ?)"

        # cursor.execute(query, (data['username'], data['password']))

        # conn.commit()
        # conn.close()
        try:
            user = UserModel(data['username'], data['password'])
            user.save_to_db()
        except:
            return {'status': 'Error', 'code': 500, 
                'reason': 'An error occurred while registering user account.'
                }, 500

        return {"message": "User created successfully."}, 201