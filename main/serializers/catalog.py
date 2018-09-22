# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class CatalogSchema(Schema):
    name = fields.String(required=True)
