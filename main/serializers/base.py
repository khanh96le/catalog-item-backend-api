# -*- coding: utf-8 -*-


import logging

from marshmallow import Schema

from main.exceptions import InvalidSchema


class BaseSchema(Schema):
    def handle_error(self, error, data):
        """Log and raise our custom exception when (de)serialization fails."""

        logging.error(error.messages)
        raise InvalidSchema.invalid_schema(error.message)

    class Meta:
        strict = True
