# -*- coding: utf-8 -*-
from marshmallow import fields, post_dump

from main.serializers.base import BaseSchema
from main.serializers.user import UserSchema


class CommentSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    body = fields.String(required=True)

    user = fields.Nested(UserSchema, dump_only=True)

    # For envelop
    comment = fields.Nested('self', exclude=('comment',), default=True, load_only=True)

    @post_dump
    def dump_comment(self, data):
        data['author'] = data['user']['user']
        return {'comment': data}


class CommentsSchema(CommentSchema):
    @post_dump(pass_many=True)
    def dump_comments(self, data, many):
        return {'comments': data, 'commentsCount': len(data)}
