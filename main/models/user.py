from main.databases import Model
from main.extensions import db
from main.libs import bcrypt_custom


class UserModel(Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))
    password_salt = db.Column(db.String(64))
    google_id = db.Column(db.String(32), unique=True)
    image_url = db.Column(db.String(500))
    token = db.Column(db.String(256))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

        if kwargs.get('password'):
            self.set_password(kwargs.get('password'))

    def set_password(self, password):
        self.password, self.password_salt = \
            bcrypt_custom.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt_custom.check_password_hash(
            self.password, self.password_salt, value
        )
