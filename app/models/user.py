from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    image_url = db.Column(db.String(10000))
    family_name = db.Column(db.String(50))
    given_name = db.Column(db.String(50))
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, family_name, given_name, email, google_id, image_url):
        self.family_name = family_name
        self.given_name = given_name
        self.email = email
        self.google_id = google_id
        self.image_url = image_url
        self.name = self.given_name + self.family_name

    def json(self):
        return {
            'name': self.name,
            'image_url': self.image_url
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

