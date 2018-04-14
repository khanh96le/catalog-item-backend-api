from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, id):
        store = StoreModel.find_by_id(id)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self):
        data = Store.parser.parse_args()
        name = data['name']
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(
                name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def put(self, id):
        store = StoreModel.find_by_id(id)

        if not store:
            return {'message': "A store with id '{}' is not exist.".format(
                id)}, 400

        name = Store.parser.parse_args()['name']
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(
                name)}, 400

        store.name = name

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 200


    def delete(self, id):
        store = StoreModel.find_by_id(id)
        if store:
            store.delete_from_db()

        return store.json(), 204


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
