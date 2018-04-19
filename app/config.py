import os
from datetime import timedelta


class Config:
    # secrete key for encoding and decoding access token
    # TODO: Move hard code config into ENV config
    SECRET_KEY = 'REPLACE THIS WITH SUPER SECRET KEY'

    # living time of access token is 1 year
    JWT_EXPIRATION_DELTA = timedelta(seconds=60*60*24*365)


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
