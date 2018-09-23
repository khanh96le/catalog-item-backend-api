# -*- coding: utf-8 -*-

import logging

from marshmallow import Schema, fields

from main.exceptions import InvalidSchema


class CatalogSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    def handle_error(self, error, data):
        """Return custom error."""

        logging.error(error.messages)
        raise InvalidSchema.invalid_schema(error.message)

    class Meta:
        strict = True
