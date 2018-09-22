from flask import request, Blueprint
from flask_apispec import use_kwargs
from werkzeug.exceptions import BadRequest

from main.extensions import db
from main.models.catalog import CatalogModel
from main.serializers.catalog import CatalogSchema

blueprint = Blueprint('catalog', __name__)


@blueprint.route('/catalogs/<int:catalog_id>', methods=('GET',))
def get_catalog(catalog_id):
    """Find a catalog by its ID. Response json format if catalog
    exists, unless response 404 not found.
    """
    catalog = CatalogModel.find_by_id(catalog_id)
    if not catalog:
        return {'message': 'Catalog {} not found'.format(catalog_id)}, 404
    return catalog.json()


@blueprint.route('/catalogs/<int:catalog_id>', methods=('PUT',))
def update_catalog(catalog_id):
    """Update a catalog by modifying its name. Validate before
    updating.
    """
    try:
        data = CatalogModel.validate(request.json)
    except ValueError as e:
        return dict(message=str(e)), 400

    catalog = CatalogModel.find_by_id(catalog_id)
    if not catalog:
        return dict(message='Catalog {} not found.'
                    .format(catalog_id)), 404

    name = data.name
    if CatalogModel.find_by_name(name):
        return dict(message='Catalog name "{}" already exists.'
                    .format(name)), 400

    catalog.name = name
    catalog.save_to_db()
    return catalog.json(), 200


@blueprint.route('/catalogs/<int:catalog_id>', methods=('DELETE',))
def delete_catalog(catalog_id):
    """Delete a catalog by its ID."""
    catalog = CatalogModel.find_by_id(catalog_id)
    if not catalog:
        return {'message': 'Catalog {} not found.'.format(catalog_id)}, 404

    catalog.delete_from_db()
    return {'message': 'Deleted successful.'}, 200


@blueprint.route('/catalogs', methods=('GET',))
def get_catalogs():
    """Find catalogs have name contains a specific string."""
    catalogs = CatalogModel.query.all()
    return {'catalogs': [catalog.json() for catalog in catalogs]}


@blueprint.route('/catalogs', methods=('POST',))
@use_kwargs(CatalogSchema())
def create_catalog(**kwargs):
    """Create new catalog."""
    data = request.json
    catalog = CatalogModel.query.filter_by(name=data.get('name')).one_or_none()

    if catalog:
        raise BadRequest()

    catalog = CatalogModel(**kwargs)
    db.session.add(catalog)
    db.session.commit()
    return None
