from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with

from main.exceptions import InvalidUsage
from main.models.user import UserModel
from main.serializers.user import UserSchema

blueprint = Blueprint('user', __name__)


@blueprint.route('/users', methods=('POST',))
@use_kwargs(UserSchema())
@marshal_with(UserSchema())
def register_user_by_email(**kwargs):
    """Register user by email password."""

    # Verify email
    user = UserModel.query.filter_by(email=kwargs.get('email')).one_or_none()
    if user:
        raise InvalidUsage.user_already_existed()

    return UserModel(**kwargs).save(), 201

# @blueprint.route('/users/auth/google', methods=('POST',))
# def register_user_with_google():
#     """Receive token ID from client, verify with Google account.
#     If account already exists, log user in.
#     If account doesn't exist, create new account and log user in.
#     """
#     try:
#         token_id = UserLogin.parser.parse_args()['tokenId']
#         profile_str = UserLogin.parser.parse_args()['profileObj']
#     except:
#         return {'message': 'Not found authentication info'}, 404
#
#     profile = ast.literal_eval(profile_str)
#     url = ('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s'
#            % token_id)
#     h = httplib2.Http()
#     result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
#
#     # verify result
#     if not ('email' in result.keys() and 'sub' in result.keys()):
#         return {'message': 'Token id is invalid'}
#
#     # verify email
#     if profile['email'] != result['email']:
#         return {'message': 'Invalid email'}, 404
#
#     # verify gplus id
#     if profile['googleId'] != result['sub']:
#         return {'message': 'Invalid gplus id'}, 404
#
#     # check user in database,
#     # if not exist, create new user then generate access token
#     # else generate access token
#     user = UserModel.query.filter_by(email=result['email']).first()
#     if not user:
#         user = UserModel(
#             family_name=result['family_name'],
#             given_name=result['given_name'],
#             email=result['email'],
#             google_id=result['sub'],
#             image_url=result['picture']
#         )
#         user.save_to_db()
#
#     # generate JWT token
#     # token = _default_jwt_encode_handler(user)
#     token = 'abc'
#
#     return {'user': user.json(),
#             'access_token': token.decode('utf-8')}, 200
