# -*- coding: utf-8 -*-
from marshmallow import fields

from main.serializers.base import BaseSchema
from main.serializers.user import UserSchema


class ArticleSchema(BaseSchema):
    title = fields.String(required=True)
    slug = fields.String()
    content = fields.String(required=True)

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True, required=True)
    updated_at = fields.DateTime(dump_only=True, required=True)

    user = fields.Nested(UserSchema, dump_only=True)
