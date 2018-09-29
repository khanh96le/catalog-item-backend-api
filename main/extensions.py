# -*- coding: utf-8 -*-
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
