import ast
import json
import httplib2
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('tokenId', type=str)
    parser.add_argument('profileObj', type=str)

    def post(self):
        try:
            token_id = UserLogin.parser.parse_args()['tokenId']
            profileStr = UserLogin.parser.parse_args()['profileObj']
        except:
            return {"message": "Not found authentication info"}

        profile = ast.literal_eval(profileStr)
        url = ('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s'
               % token_id)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

        # verify result
        if not ('email' in result.keys() and 'sub' in result.keys()):
            return {"message": "Token ID is invalid"}

        # verify email
        if profile['email'] != result['email']:
            return {"message": "Invalid email"}, 404

        # verify gplus id
        if profile['googleId'] != result['sub']:
            return {"message": "Invalid gplus id"}, 404

        # TODO: Check user in database

        return {"message": "Login success"}, 200