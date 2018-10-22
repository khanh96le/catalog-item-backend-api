# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_apispec import marshal_with

from main.exceptions import InvalidUsage
from main.models.article import ArticleModel
from main.serializers.comment import CommentsSchema

blueprint = Blueprint('comment', __name__)


@blueprint.route('/articles/<slug>/comments', methods=['GET'])
@marshal_with(CommentsSchema(many=True))
def get_comments(slug):
    article = ArticleModel.query.filter_by(slug=slug).one_or_none()

    if not article:
        raise InvalidUsage.article_not_found()

    return article.comments
