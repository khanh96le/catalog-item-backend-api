from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_restful import Api

from app.resources.catalog import Catalog, CatalogList
from app.resources.item import Item, ItemList
from app.resources.user import UserRegister, UserLogin
from app.security import authenticate, identity


def create_app(object_name):
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    jwt = JWT(app, authenticate, identity)

    app.config.from_object(object_name)

    api.add_resource(Catalog, '/api/catalog', '/api/catalog/<int:id>')
    api.add_resource(CatalogList, '/api/catalogs')
    api.add_resource(Item, '/api/item', '/api/item/<int:id>')
    api.add_resource(ItemList, '/api/items')

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/api/login')

    return app
