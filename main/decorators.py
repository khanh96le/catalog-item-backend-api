from functools import wraps

import jwt
from flask import request, current_app

from app.models.errors import UnauthorizedError


def auth_enabled(is_required=True):
    """
    Check access token if it's required and then decode it.
    :param is_required: boolean
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            access_token = request.headers.get('Authorization')

            if is_required:
                if access_token is None:
                    raise UnauthorizedError(
                        'Authorization Required',
                        description='Request does not contain access token'
                    )

            if access_token is not None:
                try:
                    payload = jwt.decode(
                        access_token,
                        key=current_app.config['SECRET_KEY'],
                        algorithms=['HS256'])
                    kwargs['user_info'] = payload
                except Exception as e:
                    raise UnauthorizedError(
                        'Access token is invalid',
                        description='Access token is invalid'
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator
