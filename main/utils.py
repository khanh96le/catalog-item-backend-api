# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_admin import Admin

NAME = 'micro_blog'
TEMPLATE_MODE = 'adminlte'


class AdminBlueprint(Blueprint):
    views = None

    def __init__(self, *args, **kargs):
        self.views = []
        super(AdminBlueprint, self).__init__(
            'admin2', __name__,
            url_prefix='/admin2',
            static_folder='static',
            static_url_path='/static/admin'
        )

    def add_view(self, view):
        self.views.append(view)

    def register(self, app, options, first_registration=False):
        admin = Admin(app, name=NAME, template_mode=TEMPLATE_MODE)

        for v in self.views:
            admin.add_view(v)

        return super(AdminBlueprint, self).register(app, options, first_registration)
