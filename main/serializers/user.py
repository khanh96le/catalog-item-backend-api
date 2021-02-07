# -*- coding: utf-8 -*-

from marshmallow import fields, validate, post_dump

from .base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(load_only=True, required=True,
                             validate=validate.Length(min=8))
    google_id = fields.String()
    image_url = fields.String()
    token = fields.String()
    bio = fields.String()

    @post_dump()
    def make_comment(self, data):
        return {'user': data}


class SignInEmailSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
