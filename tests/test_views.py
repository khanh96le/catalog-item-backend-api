# -*- coding: utf-8 -*-
import json

import pytest

from main.app import create_app
from main.config import TestConfig
from main.extensions import db


def get_api_headers(access_token=None):
    return {
        # 'Authorization': 'JWT ' + access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture(scope='function')
def app():
    """Create test app instance"""
    return create_app(TestConfig)


@pytest.fixture(scope='function')
def testclient(app):
    """Create test client to call API without serving a HTTP web server."""
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def create_database(app):
    """Init test database"""
    db.app = app
    # db.init_app(app)
    with app.app_context():
        db.create_all()

    yield db

    db.session.close()
    db.drop_all()


def test_create_catalog(testclient):
    headers = get_api_headers()
    data = json.dumps({
        'name': 'Music'
    })

    res = testclient.post(
        '/catalogs',
        headers=headers,
        data=data,
        content_type='application/json'
    )
    assert res.status_code == 200
