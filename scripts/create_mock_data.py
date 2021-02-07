# -*- coding: utf-8 -*-
from main.models.article import ArticleModel
from main.models.catalog import CatalogModel
from main.models.user import UserModel


def create_admin():
    # Create user
    user = UserModel(
        username='admin',
        email='admin@email.com',
        password='123456789',
    )
    user.save()


def create_catalogs():
    # Create catalogs
    sample_catalogs = ['Python', 'Javascript', 'Database', 'Clean Code']
    for catalog in sample_catalogs:
        CatalogModel(
            name=catalog
        ).save()


def create_articles():
    # Create articles
    sample_articles = [
        ('Python is awesome', 'Python is awesome, python number 1'),
        ('Javascript is awesome', 'Javascript is awesome, python number 1'),
        ('Database is awesome', 'Database is awesome, python number 1'),
        ('Clean code is ...', 'Python is awesome, python number 1'),
    ]
    for article in sample_articles:
        ArticleModel(
            title=article[0],
            content=article[1],
            user_id=1
        ).save()


def create_sample_data():
    from main.app import create_app
    from main.config import config

    CONFIG = config['default']

    create_app(CONFIG)
    create_admin()
    create_catalogs()
    create_articles()
