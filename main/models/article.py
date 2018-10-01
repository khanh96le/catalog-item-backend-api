import os

from slugify import slugify

from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db


class ArticleModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'article'

    title = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(512), unique=True, nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = relationship('UserModel', backref=db.backref('articles'))

    def __init__(self, *args, **kwargs):
        # Check if the slug has already existed, if yes, we need to add some
        # extra random string to the tail of slug, if no, just do slugify
        if kwargs.get('slug'):
            slug = kwargs.get('slug')
        else:
            slug = slugify(kwargs['title'])

        article = ArticleModel.query.filter_by(slug=slug).one_or_none()
        kwargs['slug'] = slug if article else slug + '-' + os.urandom(5).hex()

        db.Model.__init__(self, *args, **kwargs)
