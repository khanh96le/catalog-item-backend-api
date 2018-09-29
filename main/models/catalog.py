from main.databases import Model
from main.extensions import db


class CatalogModel(Model):
    __tablename__ = 'catalog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
