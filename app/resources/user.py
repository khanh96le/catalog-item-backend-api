import ast
import json
import httplib2
from flask_restful import Resource, reqparse
from app.models.user import UserModel


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
    parser.add_argument('accessToken', type=str)

    def post(self):
        try:
            token_id = UserLogin.parser.parse_args()['tokenId']
            profile_str = UserLogin.parser.parse_args()['profileObj']
            access_token = UserLogin.parser.parse_args()['accessToken']
        except:
            return {"message": "Not found authentication info"}

        profile = ast.literal_eval(profile_str)
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

        # check user in database,
        # if not exist, create new user then create session
        # else create session
        query_result = UserModel.query.filter_by(email=result['email'])
        if not query_result.count():
            user = UserModel(
                family_name=result['family_name'],
                given_name=result['given_name'],
                email=result['email'],
                google_id=result['sub'],
                image_url=result['picture']
            )
            user.save_to_db()
        else:
            user = query_result.first()

        return user.json(), 200
