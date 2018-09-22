# -*- coding: utf-8 -*-
"""Provides fixtures that used in tests."""
import pytest

from main.app import create_app
from main.config import TestConfig
from main.extensions import db


@pytest.fixture(scope='function')
def test_app():
    """Create test app instance."""

    return create_app(TestConfig)


@pytest.fixture(scope='function')
def testclient(test_app):
    """Create test client to call API without serving a HTTP web server.

    Examples::

        def test_do_something(testclient):
            # POST
            testclient.post(
                '/catalogs',
                headers={},
                data={},
                content_type='application/json'
            )

            # GET
            testclient.get(
                '/catalogs',
                headers={},
                content_type='application/json'
            )
    """

    return test_app.test_client()


@pytest.fixture(scope='function', autouse=True)
def session(test_app):
    """Init test database.  Auto run when starting every new test cases.

    Example::

        def test_do_something(session):
            session.add(obj)
            session.commit()

    """

    db.app = test_app
    with test_app.app_context():
        db.create_all()

    yield db.session

    db.session.close()
    db.drop_all()
