from db import db
from app import create_app

app = create_app('app.config.DevConfig')

if __name__ == '__main__':
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
