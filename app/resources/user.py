import ast
import json
import httplib2
from flask_restful import Resource, reqparse
from flask_jwt import _default_jwt_encode_handler, jwt_required
from app.models.user import UserModel


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('tokenId', type=str)
    parser.add_argument('profileObj', type=str)

    @jwt_required()
    def get(self):
        return {'message': 'Valid token'}, 200

    @staticmethod
    def post():
        try:
            token_id = UserLogin.parser.parse_args()['tokenId']
            profile_str = UserLogin.parser.parse_args()['profileObj']
        except:
            return {'message': 'Not found authentication info'}, 404

        profile = ast.literal_eval(profile_str)
        url = ('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s'
               % token_id)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

        # verify result
        if not ('email' in result.keys() and 'sub' in result.keys()):
            return {'message': 'Token id is invalid'}

        # verify email
        if profile['email'] != result['email']:
            return {'message': 'Invalid email'}, 404

        # verify gplus id
        if profile['googleId'] != result['sub']:
            return {'message': 'Invalid gplus id'}, 404

        # check user in database,
        # if not exist, create new user then generate access token
        # else generate access token
        user = UserModel.query.filter_by(email=result['email']).first()
        if not user:
            user = UserModel(
                family_name=result['family_name'],
                given_name=result['given_name'],
                email=result['email'],
                google_id=result['sub'],
                image_url=result['picture']
            )
            user.save_to_db()

        # generate JWT token
        token = _default_jwt_encode_handler(user)

        return {'user': user.json(),
                'access_token': token.decode('utf-8')}, 200
