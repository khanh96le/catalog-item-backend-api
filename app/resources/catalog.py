from webargs import fields
from webargs.flaskparser import use_kwargs
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from app.models.catalog import CatalogModel


class Catalog(Resource):
    @staticmethod
    def get(catalog_id):
        catalog = CatalogModel.find_by_id(catalog_id)
        if not catalog:
            return {'message': 'Catalog not found'}, 404
        return catalog.json()

    @jwt_required()
    def put(self, catalog_id):
        try:
            update_catalog = CatalogModel.validate(request.json)
        except ValueError as e:
            return dict(message=str(e)), 400

        catalog = CatalogModel.find_by_id(catalog_id)
        if not catalog:
            return dict(message="A catalog with id '{}' is not found."
                        .format(id)), 404

        name = update_catalog.name
        if CatalogModel.find_by_name(name):
            return dict(message="A catalog with name '{}' already exists."
                        .format(name)), 400

        catalog.name = name
        catalog.save_to_db()
        return catalog.json(), 200

    @jwt_required()
    def delete(self, catalog_id):
        catalog = CatalogModel.find_by_id(catalog_id)
        if not catalog:
            return {'message': 'Catalog {} is not '
                               'found.'.format(catalog_id)}, 404

        catalog.delete_from_db()
        return {'message': 'Catalog deleted'}, 200


class CatalogList(Resource):
    args = {
        'name': fields.Str(
            required=False
        ),
    }

    @use_kwargs(args)
    def get(self, name):
        if name:
            catalogs = CatalogModel.find_by_names(name)
        else:
            catalogs = CatalogModel.query.all()
        return {
            'catalogs': [catalog.json() for catalog in catalogs]}

    @jwt_required()
    def post(self):
        try:
            catalog = CatalogModel.validate(request.json)
        except ValueError as e:
            return dict(message=str(e)), 400

        # check if name is existing, abort
        name = catalog.name
        if CatalogModel.find_by_name(name):
            return dict(message="A catalog with name '{}' already exists."
                        .format(name)), 400

        catalog.save_to_db()
        return catalog.json(), 201
