# -*- coding: utf-8 -*-

from flask import jsonify


def template(messages, code=500):
    return {'messages': messages, 'status_code': code}


#: Common errors
UNKNOWN_ERROR = template([], code=500)

#: Catalog errors
CATALOG_NOT_FOUND = template(['Catalog not found'], code=404)
CATALOG_ALREADY_EXISTED = template(['Catalog has already existed'], code=404)


class InvalidUsage(Exception):
    def __init__(self, messages, status_code=None, payload=None):
        Exception.__init__(self)
        self.messages = messages
        self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.messages
        return jsonify(rv)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def catalog_not_found(cls):
        return cls(**CATALOG_NOT_FOUND)

    @classmethod
    def catalog_already_existed(cls):
        return cls(**CATALOG_NOT_FOUND)
