from flask import current_app
import unittest


class APITestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_catalogs(self):
        pass
