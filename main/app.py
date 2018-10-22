from flask import Flask

from main import commands
from main.config import ProdConfig
from main.exceptions import InvalidUsage, InvalidSchema, AuthenticationError, AuthorizationError
from main.extensions import cors, db, bcrypt, migrate, jwt, admin
from main.models.article import ArticleModel
from main.models.catalog import CatalogModel
from main.models.comment import CommentModel
from main.models.control import ControlModel
from main.models.log import LogModel
from main.models.permission import PermissionModel
from main.models.role import RoleModel
from main.models.user import UserModel
from main.views import catalog, user, article, comment
from main.views.admin import RoleModelView, BaseModelView, PermissionModelView, UserModelView, ArticleModelView


def create_app(config_object=ProdConfig):
    """Application factory to produce application instance.
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
        config_object (object): the configuration loaded from `main.config`

    """

    app = Flask(__name__)

    # Ignore trailing slash in flask route
    # https://stackoverflow.com/questions/40365390/trailing-slash-in-flask-route
    app.url_map.strict_slashes = False

    # App settings
    app.config.from_object(config_object)

    # Register all extensions which are used in this application
    register_extensions(app)

    # Expose endpoints to the world
    register_blueprints(app)

    # Errors should be thrown in the same format
    register_error_handlers(app)

    # Some handy commands
    register_commands(app)

    return app


def register_extensions(app):
    """Every extensions start with flask_* will be initialized here."""

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_admin_views()
    admin.init_app(app)


def register_admin_views():
    """Register all admin views. This seem pretty awkward."""

    admin.add_view(UserModelView(UserModel, db.session))
    admin.add_view(ArticleModelView(ArticleModel, db.session))
    admin.add_view(BaseModelView(CatalogModel, db.session))
    admin.add_view(BaseModelView(CommentModel, db.session))
    admin.add_view(BaseModelView(LogModel, db.session))
    admin.add_view(RoleModelView(RoleModel, db.session))
    admin.add_view(PermissionModelView(PermissionModel, db.session))
    admin.add_view(BaseModelView(ControlModel, db.session))


def register_blueprints(app):
    """Register endpoints here.  Also do allow CORS."""

    # Allow CORS
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(catalog.blueprint, origins=origins)
    cors.init_app(article.blueprint, origins=origins)
    cors.init_app(user.blueprint, origins=origins)
    cors.init_app(comment.blueprint, origins=origins)

    # Register all endpoints in `main.views`
    app.register_blueprint(catalog.blueprint)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(article.blueprint)
    app.register_blueprint(comment.blueprint)


def register_error_handlers(app):
    """The errors should be raised in the same format."""

    def error_handler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(error_handler)
    app.errorhandler(InvalidSchema)(error_handler)
    app.errorhandler(AuthenticationError)(error_handler)
    app.errorhandler(AuthorizationError)(error_handler)


def register_commands(app):
    """Register all the command used by CLI"""

    app.cli.add_command(commands.test)
    app.cli.add_command(commands.urls)
