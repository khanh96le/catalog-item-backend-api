from db import db
import datetime


class CatalogModel(db.Model):
    __tablename__ = 'catalogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    lastUpdated = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'itemsCount': self.items.count(),
            'lastUpdated': "{}-{}-{}".format(
                self.lastUpdated.year,
                self.lastUpdated.month,
                self.lastUpdated.day),
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_names(cls, name):
        return cls.query.filter(cls.name.like('%{}%'.format(name))).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()