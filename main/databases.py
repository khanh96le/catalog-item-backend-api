# -*- coding: utf-8 -*-
from datetime import datetime

from flask_sqlalchemy import Model

from main.extensions import db


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update,
    delete) operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


db.Model = db.make_declarative_base(CRUDMixin, None)
Model = db.Model


class TimestampMixin(object):
    """Inherit this class to automatically create 2 fields: `created_at` and
    `updated_at` in the database.  The `updated_at` is updated whenever any
    fields changed.
    """

    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)
