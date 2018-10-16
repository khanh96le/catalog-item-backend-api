# -*- coding: utf-8 -*-
from main.databases import Model, PKMixin, TimestampMixin, relationship
from main.extensions import db
from main.models.assoc_tables import role_permission, role_control


class RoleModel(Model, PKMixin, TimestampMixin):
    __tablename__ = 'role'

    name = db.Column(db.String(64))
    description = db.Column(db.String(256))

    permissions = relationship(
        'PermissionModel',
        secondary=role_permission,
        back_populates='roles')

    controls = relationship('ControlModel', secondary=role_control)

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        return self.name
