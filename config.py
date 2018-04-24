import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # secrete key for encoding and decoding access token
    # TODO: Move hard code config into ENV config
    SECRET_KEY = 'REPLACE THIS WITH SUPER SECRET KEY'

    # living time of access token is 1 year
    JWT_EXPIRATION_DELTA = timedelta(seconds=60 * 60 * 24 * 365)

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'\
        .format(os.path.join(basedir, 'data-dev.db'))


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'\
        .format(os.path.join(basedir, 'data.db'))


config = {
    'develop': DevConfig,
    'test': TestConfig,
    'product': ProdConfig,

    'default': ProdConfig
}