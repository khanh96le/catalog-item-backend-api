from flask import request
from flask_restful import Resource
from app.models.item import ItemModel
from app.models.catalog import CatalogModel


class Item(Resource):
    @staticmethod
    def get(item_id):
        """Get an item by its ID."""
        item = ItemModel.find_by_id(item_id)
        if item:
            return item.json()
        return {'message': 'Item {} not found'.format(item_id)}, 404

    def delete(self, item_id):
        """Delete an item by its ID."""
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {'message': 'Item {} not found.'.format(item_id)}, 404

        item.delete_from_db()
        return {'message': 'Deleted successful'}, 200

    def put(self, item_id):
        """Edit an item. Validate data before updating."""
        try:
            update_item = ItemModel.validate(request.json)
        except ValueError as e:
            return dict(message=str(e)), 400

        item = ItemModel.find_by_id(item_id)
        if not item:
            return dict(message='Item {} not found.'.format(item_id)), 404

        catalog = CatalogModel.find_by_id(update_item.catalog_id)
        if not catalog:
            return dict(message='Catalog {} not found.'
                                ''.format(update_item.catalog_id)), 404

        item.link = update_item.link
        item.catalog_id = update_item.catalog_id
        item.description = update_item.description

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @staticmethod
    def get():
        """Get all items in database, order by descending."""
        items = ItemModel.query.order_by(ItemModel.created.desc()).all()
        return {'items': [item.json() for item in items]}

    def post(self):
        """Create new item."""
        try:
            item = ItemModel.validate(request.json)
        except ValueError as e:
            return dict(message=str(e)), 400

        catalog = CatalogModel.find_by_id(item.catalog_id)
        if not catalog:
            return dict(message='Catalog {} not found.'
                                ''.format(item.catalog_id)), 404

        item.save_to_db()
        return item.json(), 201
