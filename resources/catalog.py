from flask_restful import Resource, reqparse
from models.catalog import CatalogModel


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
            return {'message': "A catalog with name '{}' already exists.".format(
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
            return {'message': "A catalog with name '{}' already exists.".format(
                name)}, 400

        store.name = name

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the catlog."}, 500

        return store.json(), 200


    def delete(self, id):
        store = CatalogModel.find_by_id(id)
        if store:
            store.delete_from_db()

        return store.json(), 204


class CatalogList(Resource):
    def get(self):
        return {'catalogs': [store.json() for store in CatalogModel.query.all()]}
