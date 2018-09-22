# -*- coding: utf-8 -*-
import json

from main.models.catalog import CatalogModel


def get_api_headers(access_token=None):
    return {
        # 'Authorization': 'JWT ' + access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


class TestCatalogViews(object):

    def test_create_catalog(self, testclient):
        data = json.dumps({
            'name': 'Music'
        })

        res = testclient.post(
            '/catalogs',
            headers=get_api_headers(),
            data=data,
            content_type='application/json'
        )
        assert res.status_code == 201
        assert json.loads(res.data).get('name') == 'Music'

    def test_get_catalogs(self, testclient):
        CatalogModel(name='Catalog 1').save()
        CatalogModel(name='Catalog 2').save()

        res = testclient.get(
            '/catalogs',
            headers=get_api_headers(),
            content_type='application/json'
        )
        assert res.status_code == 200
        assert len(json.loads(res.data)) == 2

    def test_delete_catalog(self, testclient):
        # Test delete non-existing catalog
        res = testclient.delete(
            '/catalogs/{}'.format(1),
            headers=get_api_headers(),
            content_type='application/json'
        )
        assert res.status_code == 404
        assert json.loads(res.data)[0] == 'Catalog not found'

        # Test delete success
        catalog = CatalogModel(name='Catalog 1')
        catalog.save()

        res = testclient.delete(
            '/catalogs/{}'.format(catalog.id),
            headers=get_api_headers(),
            content_type='application/json'
        )
        assert res.status_code == 204

    def test_get_catalog(self, testclient):
        catalog = CatalogModel(name='Catalog 1')
        catalog.save()

        res = testclient.get(
            '/catalogs/{}'.format(catalog.id),
            headers=get_api_headers(),
            content_type='application/json'
        )
        assert res.status_code == 200

    def test_update_catalog(self, testclient):
        catalog = CatalogModel(name='Catalog 1')
        catalog.save()

        res = testclient.put(
            '/catalogs/{}'.format(catalog.id),
            data=json.dumps({'name': 'Catalog 2'}),
            headers=get_api_headers(),
            content_type='application/json'
        )
        assert res.status_code == 200
        assert json.loads(res.data).get('name') == 'Catalog 2'
