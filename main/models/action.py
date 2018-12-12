# -*- coding: utf-8 -*-
from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db
from main.models.assoc_tables import action_permission


class ActionModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'action'

    name = db.Column(db.String(32))

    permissions = relationship(
        'PermissionModel',
        secondary=action_permission,
        back_populates='actions')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return self.name
