# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
admin = Admin(name='microblog', template_mode='bootstrap3')


def jwt_identity(identity):
    from main.models.user import UserModel
    return UserModel.query.get(identity)


jwt = JWTManager()
jwt.user_loader_callback_loader(jwt_identity)
