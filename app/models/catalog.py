from app import db


class CatalogModel(db.Model):
    __tablename__ = 'catalog'

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

    @staticmethod
    def validate(data):
        """
        Validate data
        If data is valid, return an instance of Catalog
        If data is invalid, raise ValueError

        :param data: a dictionary
        """
        if 'name' not in data:
            raise ValueError('Catalog name is required')

        name = data['name']
        if not name:
            raise ValueError('Catalog name cannot be blank')

        if len(name) > 40:
            raise ValueError('Catalog name cannot be greater than 40 '
                             'characters')

        return CatalogModel(name=name)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_names(cls, name):
        return cls.query.filter(cls.name.like('%{}%'.format(name))).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
