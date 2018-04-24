import json
import unittest
from flask import current_app
from app import create_app, db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MjQ1NzU0MjIsImV4cCI6MTU1NjExMTQyMiwiaWF0IjoxNTI0NTc1NDIyLCJpZGVudGl0eSI6MX0.ScyQPjZ84zQr1Q4WJWzU2mouEf_k2hE_OhL4vIQl2fI"
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def get_api_headers(access_token):
        return {
            'Authorization': 'JWT ' + access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_create_catalog_without_authorize(self):
        # expect: return status code 401
        result = self.client.post(
            '/catalogs',
            data=json.dumps({'name': 'Sport'})
        )
        self.assertEqual(result.status_code, 401)

    def test_create_catalog_with_empty_name(self):
        # expect: return status code 400
        result = self.client.post(
            '/catalogs',
            headers=self.get_api_headers(self.access_token),
            data=json.dumps({'name': ''})
        )
        self.assertEqual(result.status_code, 400)
