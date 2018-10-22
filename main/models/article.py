import os

from slugify import slugify

from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db
from main.models.assoc_tables import catalog_article


class ArticleModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'article'

    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(512), unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)

    # One to many
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = relationship('UserModel', back_populates='articles')

    # Many to many
    comments = relationship('CommentModel', backref=db.backref('article'))
    catalogs = relationship('CatalogModel', secondary=catalog_article,
                            back_populates='articles')

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
