# -*- coding: utf-8 -*-

from main.extensions import db

role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

user_permission = db.Table(
    'user_permission',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

role_control = db.Table(
    'role_control',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('control_id', db.Integer, db.ForeignKey('control.id'))
)

user_control = db.Table(
    'user_control',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('control_id', db.Integer, db.ForeignKey('control.id'))
)

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

catalog_article = db.Table(
    'catalog_article',
    db.Column('catalog_id', db.Integer, db.ForeignKey('catalog.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)
