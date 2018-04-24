from db import db
from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app('app.config.DevConfig')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    manager.run()
