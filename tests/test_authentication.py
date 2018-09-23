# -*- coding: utf-8 -*-
import json

from tests.utils import get_api_headers


def _register_user(testclient):
    data = {
        'email': 'test@gmail.com',
        'password': '12345678@ABC',
    }
    return testclient.post(
        '/users',
        data=json.dumps(data),
        header=get_api_headers(),
        content_type='application/json'
    )


class TestAuthentication(object):
    def test_register_user_by_email_password(self, testclient):
        resp = _register_user(testclient)
        assert resp.status_code == 201
