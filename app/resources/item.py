from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from app.models.item import ItemModel
from app.models.catalog import CatalogModel


class Item(Resource):
    @staticmethod
    def get(item_id):
        item = ItemModel.find_by_id(item_id)
        if item:
            return item.json()
        return {'message': 'Item {} not found'.format(item_id)}, 404

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {'message': 'Item {} not found.'.format(item_id)}, 404

        item.delete_from_db()
        return {'message': 'Deleted successful'}, 200

    @jwt_required()
    def put(self, item_id):
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
        items = ItemModel.query.order_by(ItemModel.created.desc()).all()
        return {'items': [item.json() for item in items]}

    @jwt_required()
    def post(self):
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
