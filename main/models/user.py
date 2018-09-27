import bcrypt

from main.extensions import db, Model, bcrypt


class UserModel(Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    password_salt = db.Column(db.String(50))
    google_id = db.Column(db.String(20), unique=True)
    image_url = db.Column(db.String(1000))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

        if kwargs.get('password'):
            self.set_password(kwargs.get('password'))

    def set_password(self, password):
        self.password_salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(str(password), self.password_salt)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)
