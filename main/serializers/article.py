# -*- coding: utf-8 -*-
from marshmallow import fields, pre_load, post_dump, validate

from main.serializers.base import BaseSchema
from main.serializers.user import UserSchema


class ArticleSchema(BaseSchema):
    title = fields.String(required=True,
                          validate=validate.Length(min=4, max=250))
    description = fields.String()
    slug = fields.String()
    body = fields.String(required=True, validate=validate.Length(min=40))

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True, required=True)
    updated_at = fields.DateTime(dump_only=True, required=True)

    user = fields.Nested(UserSchema, dump_only=True)

    # For envelop
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)

    @pre_load
    def load_article(self, data):
        return data['article']

    @post_dump
    def dump_article(self, data):
        data['author'] = data['user']['user']
        return {'article': data}


class ArticleSchemas(ArticleSchema):

    @post_dump
    def dump_article(self, data):
        data['author'] = data['user']['user']
        return data

    @post_dump(pass_many=True)
    def dump_articles(self, data, many):
        return {'articles': data, 'articlesCount': len(data)}
