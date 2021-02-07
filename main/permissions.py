# -*- coding: utf-8 -*-
from functools import wraps

from flask_jwt_extended import current_user

from main.exceptions import AuthorizationError


def check_permission(action, resource):
    """
    A decorator to protect a Flask endpoint.

    This decorator will check in database and make sure the user has permissions
    to call that endpoint.
    """

    def decorator_check_permission(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Each role has some certain permissions
            roles = current_user.roles
            role_permissions = []
            for role in roles:
                for permission in list(role.permissions):
                    role_permissions.append(permission)

            # Some users have additional permissions beside the role permissions
            user_permissions = current_user.permissions

            # Make sure the combination of role permissions and user permissions
            # is not duplicated
            permissions = set(user_permissions + role_permissions)

            # Check if current user has permission to interact with the endpoint
            for permission in permissions:
                if (permission.action == action
                        and permission.resource == resource):
                    return fn(*args, **kwargs)
            raise AuthorizationError.invalid_permission()

        return wrapper

    return decorator_check_permission
