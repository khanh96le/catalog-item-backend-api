# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.exc import IntegrityError

from main.exceptions import InvalidUsage
from main.extensions import db
from main.models.article import ArticleModel
from main.models.comment import CommentModel
from main.permissions import check_permission
from main.serializers.comment import CommentsSchema, CommentSchema

blueprint = Blueprint('comment', __name__)


@blueprint.route('/articles/<slug>/comments', methods=['GET'])
@marshal_with(CommentsSchema(many=True))
def get_comments(slug):
    article = ArticleModel.query.filter_by(slug=slug).one_or_none()

    if not article:
        raise InvalidUsage.article_not_found()

    return article.comments


@blueprint.route('/articles/<slug>/comments', methods=['POST'])
@jwt_required
@check_permission('create', 'comment')
@use_kwargs(CommentSchema)
@marshal_with(CommentSchema)
def create_comment(slug, **kwargs):
    article = ArticleModel.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()

    try:
        comment = CommentModel(
            body=kwargs['body'],
            user_id=current_user.id,
            article_id=article.id
        )
        comment.save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.unknown_error()

    return comment, 201
