from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from app.resources.catalog import Catalog, CatalogList
from app.resources.item import Item, ItemList
from app.resources.user import UserLogin
from app.security import authenticate, identity


def create_app(object_name):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    app.config.from_object(object_name)

    JWT(app, authenticate, identity)

    api.add_resource(Catalog, '/catalogs/<int:catalog_id>')
    api.add_resource(CatalogList, '/catalogs')
    api.add_resource(Item, '/items/<int:item_id>')
    api.add_resource(ItemList, '/items')

    api.add_resource(UserLogin, '/api/login')

    return app
