# -*- coding: utf-8 -*-

from main.databases import Model, PKMixin, TimestampMixin
from main.extensions import db


class CommentModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'comment'

    content = db.Text()
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.ForeignKey('article.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
