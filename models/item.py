from db import db
import re


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000))
    created = db.Column(db.DateTime, server_default=db.func.now())
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalogs.id'))
    catalog = db.relationship('CatalogModel')

    def __init__(self, link, description, catalog_id):
        self.link = link
        self.description = description
        self.catalog_id = catalog_id

    def extract_video_id(self, link):
        regex = r"(youtu\.be\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v)\/))([^\?&\"'>]+)"
        matches = re.search(regex, link)
        try:
            video_id = matches.group(5)
            img_link = "https://img.youtube.com/vi/{}/2.jpg".format(video_id)
        except:
            return "https://img.youtube.com/vi/notexisted/2.jpg"

        return img_link

    def json(self):
        return {
            'id': self.id,
            'link': self.link,
            'img': self.extract_video_id(self.link),
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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
