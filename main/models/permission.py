# -*- coding: utf-8 -*-
from main.databases import Model, PKMixin, TimestampMixin
from main.extensions import db


class PermissionModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'permission'

    action = db.Column(db.String(16))
    resource = db.Column(db.String(32))
    description = db.Column(db.String(256))

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
