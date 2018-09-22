import pkgutil

from flask import Flask

from main.config import ProdConfig
from main.extensions import cors, db
from main.views import catalog


def create_app(config_object=ProdConfig):
    """Application factory to produce application instance.

    Args:
        config_object (object): the configuration loaded from `main.config`

    """
    app = Flask(__name__)
    # Ignore trailing slash in flask route
    # https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    # Allow CORS
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(catalog.blueprint, origins=origins)

    # Register all endpoints in `main.views`
    app.register_blueprint(catalog.blueprint)
