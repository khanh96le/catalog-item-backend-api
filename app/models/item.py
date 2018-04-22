from db import db
from app.utils import extract_video_thumbnail


class ItemModel(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))
    created = db.Column(db.DateTime, server_default=db.func.now())
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))
    catalog = db.relationship('CatalogModel')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('UserModel')

    def __init__(self, link, description, catalog_id):
        self.link = link
        self.description = description
        self.catalog_id = catalog_id

    def json(self):
        return {
            'id': self.id,
            'link': self.link,
            'img': extract_video_thumbnail(self.link),
            'description': self.description,
            'catalog': self.catalog.name,
            'created': "{}-{}-{} {}:{}:{}".format(
                self.created.year,
                self.created.month,
                self.created.day,
                self.created.hour,
                self.created.minute,
                self.created.second,
            ),
        }

    @classmethod
    def find_by_link(cls, link):
        return cls.query.filter_by(link=link).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
