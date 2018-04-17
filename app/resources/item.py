from flask_restful import Resource, reqparse
from app.models.item import ItemModel


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

    # @jwt_required(k)
    def get(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self):
        data = Item.parser.parse_args()

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}, 204

    def put(self, id):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_id(id)

        if item is None:
            return {'message': 'Item not found'}, 404
        else:
            item.link = data['link']
            item.description = data['description']
            item.catalog_id = data['catalog_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.order_by(ItemModel.created.desc()).all()
        return {'items': [item.json() for item in items]}

