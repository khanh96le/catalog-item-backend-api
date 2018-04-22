from flask_restful import Resource, reqparse
from app.models.item import ItemModel
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('link',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help="Description."
                        )
    parser.add_argument('catalog_id',
                        type=str,
                        required=True,
                        help="Every item needs a catalog id."
                        )

    @staticmethod
    def get(_id):
        item = ItemModel.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self):
        data = Item.parser.parse_args()

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}, 204

    @jwt_required()
    def put(self, _id):
        item = ItemModel.find_by_id(_id)
        if item is None:
            return {'message': 'Item not found'}, 404

        data = Item.parser.parse_args()
        item.link = data['link']
        item.description = data['description']
        item.catalog_id = data['catalog_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json()


class ItemList(Resource):
    @staticmethod
    def get():
        items = ItemModel.query.order_by(ItemModel.created.desc()).all()
        return {'items': [item.json() for item in items]}
