# -*- coding: utf-8 -*-

from main.databases import Model, PKMixin, TimestampMixin
from main.extensions import db


class LogModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'log'

    action = db.Column(db.String(16))
    resource = db.Column(db.String(32))
    old_value = db.Text()
    new_value = db.Text()
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
