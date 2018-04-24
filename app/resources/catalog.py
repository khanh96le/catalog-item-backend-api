from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from app.models.catalog import CatalogModel
from webargs import fields
from webargs.flaskparser import use_kwargs


class Catalog(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @staticmethod
    def get(catalog_id):
        catalog = CatalogModel.find_by_id(catalog_id)
        if catalog:
            return catalog.json()
        return {'message': 'Catalog not found'}, 404

    @jwt_required()
    def put(self, catalog_id):
        catalog = CatalogModel.find_by_id(catalog_id)

        # check if catalog is existing
        if not catalog:
            return dict(message="A catalog with id '{}' is not exist."
                        .format(id)), 400

        # check if catalog's name is existing
        name = Catalog.parser.parse_args()['name']
        if CatalogModel.find_by_name(name):
            return dict(message="A catalog with name '{}' already exists."
                        .format(name)), 400

        # update catalog
        catalog.name = name
        try:
            catalog.save_to_db()
        except:
            return {"message": "An error occurred creating the catalog."}, 500

        return catalog.json(), 200

    @jwt_required()
    def delete(self, catalog_id):
        catalog = CatalogModel.find_by_id(catalog_id)
        if catalog:
            catalog.delete_from_db()

        return {'message': 'Catalog deleted'}, 204


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
        data = Catalog.parser.parse_args()
        name = data['name']
        if CatalogModel.find_by_name(name):
            return dict(message="A catalog with name '{}' already exists."
                        .format(name)), 400

        catalog = CatalogModel(name)
        try:
            catalog.save_to_db()
        except:
            return {"message": "An error occurred creating the catalog."}, 500

        return catalog.json(), 201

