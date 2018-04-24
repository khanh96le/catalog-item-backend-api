from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.resources.catalog import Catalog, CatalogList
from app.resources.item import Item, ItemList
from app.resources.user import UserLogin
from app.security import authenticate, identity
from config import config


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    app.config.from_object(config[config_name])

    JWT(app, authenticate, identity)

    # db.app = app
    db.init_app(app)

    api.add_resource(Catalog, '/catalogs/<int:catalog_id>')
    api.add_resource(CatalogList, '/catalogs')
    api.add_resource(Item, '/items/<int:item_id>')
    api.add_resource(ItemList, '/items')

    api.add_resource(UserLogin, '/login')

    return app
