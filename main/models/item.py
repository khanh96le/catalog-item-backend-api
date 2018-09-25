# from app import db
# from app.utils import extract_video_thumbnail
#
#
# class ItemModel(db.Model):
#     __tablename__ = 'item'
#
#     id = db.Column(db.Integer, primary_key=True)
#     link = db.Column(db.String(1000), nullable=False)
#     description = db.Column(db.String(1000))
#     created = db.Column(db.DateTime, server_default=db.func.now())
#     catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))
#     catalog = db.relationship('CatalogModel')
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('UserModel')
#
#     def __init__(self, link, description, catalog_id):
#         self.link = link
#         self.description = description
#         self.catalog_id = catalog_id
#
#     def json(self):
#         return {
#             'id': self.id,
#             'link': self.link,
#             'img': extract_video_thumbnail(self.link),
#             'description': self.description,
#             'catalog': self.catalog.name,
#             'created': self.created.strftime('%d/%m/%y %H:%M:%S'),
#         }
#
#     @staticmethod
#     def validate(data):
#         """
#         Validate data.
#         If data is valid, return an instance of Item
#         If data is invalid, raise ValueError
#
#         :param data: a dictionary
#         """
#         if 'link' not in data or 'catalog_id' not in data:
#             raise ValueError('Link and catalog id cannot be blank')
#
#         link = data['link']
#         catalog_id = data['catalog_id']
#
#         if not link or not catalog_id:
#             raise ValueError('Link and catalog id cannot be blank')
#
#         if type(catalog_id).__name__ != 'int':
#             raise ValueError('Catalog id must be a number')
#
#         description = ''
#         if 'description' in data:
#             description = data['description']
#             if len(description) > 1000:
#                 raise ValueError('Description must be a less than 1000 '
#                                  'characters')
#
#         return ItemModel(
#             link=link,
#             catalog_id=catalog_id,
#             description=description
#         )
#
#     @classmethod
#     def find_by_link(cls, link):
#         return cls.query.filter_by(link=link).first()
#
#     @classmethod
#     def find_by_id(cls, _id):
#         return cls.query.filter_by(id=_id).first()
#
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
