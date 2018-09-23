from main.extensions import db, Model


class UserModel(Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    password_salt = db.Column(db.String(10))
    image_url = db.Column(db.String(10000))
    family_name = db.Column(db.String(50))
    given_name = db.Column(db.String(50))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
