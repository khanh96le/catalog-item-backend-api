# -*- coding: utf-8 -*-

from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db


class CommentModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'comment'

    body = db.Text()

    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = relationship('UserModel', back_populates='comments')

    article_id = db.Column(db.ForeignKey('article.id'), nullable=False)
    article = relationship('ArticleModel', back_populates='comments')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
