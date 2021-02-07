# -*- coding: utf-8 -*-
from main.databases import Model, PKMixin, TimestampMixin
from main.extensions import db


class ControlModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'control'

    element_id = db.Column(db.String(128))
    element_class = db.Column(db.String(128))
    description = db.Column(db.String(256))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
