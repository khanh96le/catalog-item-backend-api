import os


class Config:
    SECRET_KEY = 'REPLACE THIS WITH SUPER SECRET KEY'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
