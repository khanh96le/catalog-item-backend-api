# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.exc import IntegrityError

from main.exceptions import InvalidUsage
from main.extensions import db
from main.models.article import ArticleModel
from main.permissions import check_permission
from main.serializers.article import ArticleSchema, ArticleSchemas

blueprint = Blueprint('article', __name__)


@blueprint.route('/articles', methods=['POST'])
@jwt_required
@check_permission('create', 'article')
@use_kwargs(ArticleSchema())
@marshal_with(ArticleSchema())
def create_article(**kwargs):
    try:
        kwargs['user_id'] = current_user.id
        article = ArticleModel(**kwargs).save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.article_slug_already_existed()

    return article, 201


@blueprint.route('/articles', methods=['GET'])
@marshal_with(ArticleSchemas(many=True))
def get_articles():
    articles = ArticleModel.query.all()
    return articles


@blueprint.route('/articles/feed', methods=['GET'])
@jwt_required
@marshal_with(ArticleSchemas(many=True))
def get_feed():
    articles = ArticleModel.query.filter_by(user_id=current_user.id).all()
    return articles


@blueprint.route('/articles/<slug>', methods=['GET'])
@marshal_with(ArticleSchema())
def get_article(slug):
    article = ArticleModel.query.filter_by(slug=slug).first_or_404()
    return article


@blueprint.route('/articles/<slug>', methods=['PUT'])
@jwt_required
@use_kwargs(ArticleSchema())
@marshal_with(ArticleSchema())
def update_article(slug, **kwargs):
    article = ArticleModel.query.filter_by(
        slug=slug, user_id=current_user.id
    ).one_or_none()

    if not article:
        raise InvalidUsage.article_not_found()

    try:
        article.update(**kwargs)
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.article_slug_already_existed()

    return article


@blueprint.route('/articles/<slug>', methods=['DELETE'])
@jwt_required
def delete_article(slug):
    article = ArticleModel.query.filter_by(
        slug=slug, user_id=current_user.id
    ).one_or_none()

    if not article:
        raise InvalidUsage.article_not_found()

    try:
        article.delete()
    except IntegrityError:
        db.session.rollback()
        raise IntegrityError

    return '', 204
