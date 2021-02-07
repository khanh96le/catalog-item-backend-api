# -*- coding: utf-8 -*-
# DEPRECATED: Just need to remove in the future

from marshmallow import fields, post_dump

from .base import BaseSchema


class CatalogSchema(BaseSchema):
    # id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    @post_dump(pass_many=True)
    def make_comment(self, data, many):
        return {'tags': data}
