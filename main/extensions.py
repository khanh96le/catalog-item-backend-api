# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Allow cross origin
cors = CORS()

# ORM
db = SQLAlchemy()

# Security
bcrypt = Bcrypt()

# Database migration
migrate = Migrate()

# Admin panel
admin = Admin(name='microblog', template_mode='bootstrap3')


def jwt_identity(identity):
    from main.models.user import UserModel
    return UserModel.query.get(identity)


# Security
jwt = JWTManager()
jwt.user_loader_callback_loader(jwt_identity)

# Flask-login
login = LoginManager()


@login.user_loader
def user_loader(id):
    from main.models.user import UserModel
    return UserModel.query.get(id)
