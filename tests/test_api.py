import json
import unittest
from flask import current_app
from flask_jwt import _default_jwt_encode_handler
from app import create_app, db
from app.models.user import UserModel


class APITestCase(unittest.TestCase):
    def setUp(self):
        # create flask app instance in Testing mode
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

        # create a default user with id=1 to test database
        user = UserModel(
            email="email@gotitapp.co",
            google_id="12345",
            image_url="http://image.png",
            family_name="Le",
            given_name="Jerry"
        )
        db.session.add(user)
        db.session.commit()

        # get access token
        user = db.session.query(UserModel).first()
        self.access_token = _default_jwt_encode_handler(user).decode('utf-8')

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.access_token = ''

    @staticmethod
    def get_api_headers(access_token):
        return {
            'Authorization': 'JWT ' + access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }


class CatalogTestCase(APITestCase):
    def create_catalog(self,
                       headers=None,
                       data=None):
        if headers is None:
            headers = self.get_api_headers(self.access_token)
        data_json = json.dumps(data)

        return self.client.post(
            '/catalogs',
            headers=headers,
            data=data_json
        )

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_create_catalog_without_authorize(self):
        result = self.client.post(
            '/catalogs',
            data=json.dumps({'name': 'Sport'})
        )
        self.assertEqual(result.status_code, 401)

    def test_create_catalog_with_empty_name(self):
        result = self.create_catalog(data={'name': ''})
        message = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 400)
        self.assertEqual(message['message'], "Catalog name cannot be blank")

    def test_create_catalog_with_name_greater_than_40_characters(self):
        result = self.create_catalog(
            data={'name': 'This is a name with length greater than 40 '
                          'characters. In this case, API should return '
                          'status code of 400'})
        message = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 400)
        self.assertEqual(message['message'], "Catalog name cannot be greater "
                                             "than 40 characters")

    def test_create_catalog_success(self):
        result = self.create_catalog(data={'name': 'Valid Name'})

        self.assertEqual(result.status_code, 201)

    def test_create_catalog_with_existing_name(self):
        self.create_catalog(data={'name': 'Valid Name'})
        result = self.create_catalog(data={'name': 'Valid Name'})

        self.assertEqual(result.status_code, 400)

    def test_delete_catalog_not_existing(self):
        result = self.client.delete(
            '/catalogs/1',
            headers=self.get_api_headers(self.access_token)
        )
        message = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 404)
        self.assertEqual(message['message'], "Catalog 1 not found.")

    def test_delete_catalog_success(self):
        self.create_catalog(data={'name': 'Valid Name'})
        result = self.client.delete(
            '/catalogs/1',
            headers=self.get_api_headers(self.access_token)
        )

        self.assertEqual(result.status_code, 200)

    def test_edit_catalog_not_existing(self):
        result = self.client.put(
            '/catalogs/1',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Valid Name'})
        )
        message = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 404)
        self.assertEqual(message['message'], 'Catalog 1 not found.')

    def test_edit_catalog_with_existing_name(self):
        self.create_catalog(data={'name': 'Valid Name'})
        result = self.client.put(
            '/catalogs/1',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Valid Name'})
        )
        message = json.loads(result.data.decode('utf-8'))

        self.assertEqual(result.status_code, 400)
        self.assertEqual(message['message'], 'Catalog name "Valid Name" '
                                             'already exists.')

    def test_edit_catalog_success(self):
        self.create_catalog(data={'name': 'Valid Name'})
        result = self.client.put(
            '/catalogs/1',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Other Valid Name'})
        )

        self.assertEqual(result.status_code, 200)

    def test_get_catalog_last_update_field(self):
        result = self.create_catalog(data={'name': 'Valid Name'})
        data = json.loads(result.data.decode('utf-8'))
        self.assertTrue(data['lastUpdated'] is not None)


class ItemTestCase(APITestCase):
    def create_item(self,
                    headers=None,
                    data=None):
        if headers is None:
            headers = self.get_api_headers(self.access_token)
        data_json = json.dumps(data)

        return self.client.post(
            '/items',
            headers=headers,
            data=data_json
        )

    def test_create_item_without_authorize(self):
        result = self.client.post(
            'items',
            data=json.dumps({})
        )

        self.assertEqual(result.status_code, 401)

    def test_create_item_with_invalid_data(self):
        # empty link
        result = self.create_item(data={
            'description': 'Item description',
            'catalog_id': 1
        })
        self.assertEqual(result.status_code, 400)

        # empty catalog_id
        result = self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
        })
        self.assertEqual(result.status_code, 400)

        # catalog id is not number
        result = self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
            'catalog_id': 'abc'
        })
        self.assertEqual(result.status_code, 400)

    def test_create_item_with_not_existing_catalog_id(self):
        result = self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
            'catalog_id': 1
        })
        self.assertEqual(result.status_code, 404)

    def test_create_item_success(self):
        self.client.post(
            '/catalogs',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Valid Name'})
        )
        result = self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
            'catalog_id': 1
        })
        self.assertEqual(result.status_code, 201)

    def test_delete_item_not_existing(self):
        result = self.client.delete(
            '/items/1',
            headers=self.get_api_headers(self.access_token)
        )

        self.assertEqual(result.status_code, 404)

    def test_delete_item_success(self):
        self.client.post(
            '/catalogs',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Valid Name'})
        )
        self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
            'catalog_id': 1
        })
        result = self.client.delete(
            '/items/1',
            headers=self.get_api_headers(self.access_token)
        )
        self.assertEqual(result.status_code, 200)

    def test_edit_item_not_existing(self):
        result = self.client.put(
            'items/1',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({
                'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
                'description': 'Item description',
                'catalog_id': 1
            })
        )
        self.assertEqual(result.status_code, 404)

    def test_edit_item_with_not_existing_catalog_id(self):
        self.client.post(
            '/catalogs',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Valid Name'})
        )
        self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
            'catalog_id': 1
        })
        result = self.client.put(
            'items/1',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({
                'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
                'description': 'Item description',
                'catalog_id': 2
            })
        )
        self.assertEqual(result.status_code, 404)

    def test_edit_item_success(self):
        self.client.post(
            '/catalogs',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Valid Name'})
        )
        self.client.post(
            '/catalogs',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': 'Other Valid Name'})
        )
        self.create_item(data={
            'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
            'description': 'Item description',
            'catalog_id': 1
        })
        result = self.client.put(
            'items/1',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({
                'link': 'https://www.youtube.com/watch?v=SzJ46YA_RaA',
                'description': 'Item description New',
                'catalog_id': 2
            })
        )
        self.assertEqual(result.status_code, 200)
