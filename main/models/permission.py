# -*- coding: utf-8 -*-
from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db
from main.models.assoc_tables import role_permission, action_permission


class PermissionModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'permission'

    resource = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(256))

    roles = relationship(
        'RoleModel',
        secondary=role_permission,
        back_populates='permissions')

    actions = relationship(
        'ActionModel',
        secondary=action_permission,
        back_populates='permissions')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return self.resource
