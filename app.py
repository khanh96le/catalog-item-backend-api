import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.user import UserLogin
from resources.item import Item, ItemList
from resources.catalog import Catalog, CatalogList

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Catalog, '/api/catalog', '/api/catalog/<int:id>')
api.add_resource(CatalogList, '/api/catalogs')
api.add_resource(Item, '/api/item', '/api/item/<int:id>')
api.add_resource(ItemList, '/api/items')

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/api/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
