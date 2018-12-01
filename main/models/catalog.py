from main.databases import Model, TimestampMixin, PKMixin, relationship
from main.extensions import db
from main.models.assoc_tables import catalog_article


class CatalogModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'catalog'

    name = db.Column(db.String(80))
    description = db.Column(db.String(256))

    articles = relationship('ArticleModel', secondary=catalog_article,
                            back_populates='catalogs')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return self.name
