from flask_restful import Resource, reqparse
from models.catalog import CatalogModel
from flask import session
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser


class Catalog(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, id):
        store = CatalogModel.find_by_id(id)
        if store:
            return store.json()
        return {'message': 'Catalog not found'}, 404

    def post(self):
        data = Catalog.parser.parse_args()
        name = data['name']
        if CatalogModel.find_by_name(name):
            return {
                       'message': "A catalog with name '{}' already exists.".format(
                           name)}, 400

        store = CatalogModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the catalog."}, 500

        return store.json(), 201

    def put(self, id):
        store = CatalogModel.find_by_id(id)

        if not store:
            return {'message': "A catalog with id '{}' is not exist.".format(
                id)}, 400

        name = Catalog.parser.parse_args()['name']
        if CatalogModel.find_by_name(name):
            return {
                       'message': "A catalog with name '{}' already exists.".format(
                           name)}, 400

        store.name = name

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the catlog."}, 500

        return store.json(), 200

    def delete(self, id):
        catalog = CatalogModel.find_by_id(id)
        if catalog:
            catalog.delete_from_db()

        return '', 204


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


