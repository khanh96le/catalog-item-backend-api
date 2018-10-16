# -*- coding: utf-8 -*-
"""
This module defines the ModelView classes. ModelView classes decides how the
data in Admin page is shown
"""
from flask import url_for, request
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect


class BaseModelView(ModelView):
    column_display_pk = True
    column_searchable_list = ('id',)
    column_display_all_relations = True

    def __init__(self, model, session):
        super().__init__(model, session)

    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class RoleModelView(BaseModelView):
    column_list = ('id', 'created_at', 'updated_at', 'name', 'description',
                   'permissions', 'controls')
    column_searchable_list = ('name', 'id')

    def __init__(self, model, session):
        super().__init__(model, session)


class PermissionModelView(BaseModelView):
    column_list = ('id', 'created_at', 'updated_at', 'action', 'resource',
                   'description', 'roles')
    column_searchable_list = ('id', 'action', 'resource')

    def __init__(self, model, session):
        super().__init__(model, session)


class UserModelView(BaseModelView):
    column_list = ('id', 'created_at', 'updated_at', 'username', 'email',
                   'google_id', 'image_url', 'roles', 'permissions')
    column_searchable_list = ('id', 'username', 'email')

    def __init__(self, model, session):
        super().__init__(model, session)


class ArticleModelView(BaseModelView):
    column_list = ('id', 'created_at', 'updated_at', 'title', 'slug', 'user')
    column_searchable_list = ('id', 'title', 'slug', 'user_id')
    can_create = False
    can_edit = False

    def __init__(self, model, session):
        super().__init__(model, session)
