# coding: utf-8
"""
Blueprint utils methods
"""

import json
from collections import OrderedDict
from functools import wraps

from cerberus import Validator
from flask import jsonify, request, abort
from google.appengine.api import users

from src.requests import is_user_in_db, insert_new_user


def flask_constructor_error(message, status=500, custom_error_code=None, error_payload=None):
    """
    Construct Json Error returned message.
    """
    payload = {
        u"message": message
    }
    if error_payload:
        payload[u"payload"] = error_payload

    if custom_error_code:
        payload[u"error_code"] = custom_error_code

    return jsonify(payload), status


def flask_construct_response(item, code=200):
    """
    Construct Json response returned.
    """
    return jsonify(item), code


to_dict = lambda x: json.loads(x, encoding=u"utf8")

LIST_API_VALIDATION_SCHEMA = {
    u"filters": {
        u"type": u"dict",
        u"coerce": to_dict
    },
    u"offset": {
        u"type": u"integer",
        u"coerce": int
    },
    u"limit": {
        u"type": u"integer",
        u"coerce": int
    }
}


def flask_check_args(validation_schema):
    """

    Args:
        validation_schema (dict):  

    Returns:
        (funct): 
    """

    def decorated(funct):
        @wraps(funct)
        def wrapper(*args, **kwargs):
            args_dict = request.args.copy().to_dict()

            validator = Validator(validation_schema)
            # Check if the document is valid.
            if not validator.validate(args_dict):
                return flask_constructor_error(
                    message=u"Wrong args.",
                    custom_error_code=u"WRONG_ARGS",
                    status=422,
                    error_payload=validator.errors
                )

            kwargs[u"args"] = validator.document
            return funct(*args, **kwargs)

        return wrapper

    return decorated


def flask_check_and_inject_payload(validation_schema=None):
    def decorated(funct):

        @wraps(funct)
        def wrapper(*args, **kwargs):

            if request.headers.get(u"Content-Type") in [u"application/json"]:
                try:
                    payload_dict = json.loads(request.data, object_pairs_hook=OrderedDict, encoding=u"utf8")
                except ValueError as err:
                    return flask_constructor_error(
                        message=err.message,
                        custom_error_code=u"WRONG_PAYLOAD",
                        status=422
                    )

                if validation_schema:
                    validator = Validator(validation_schema)
                    # Check if the document is valid.
                    if not validator.validate(payload_dict):
                        return flask_constructor_error(
                            message=u"Wrong args.",
                            custom_error_code=u"WRONG_ARGS",
                            status=422,
                            error_payload=validator.errors
                        )

                kwargs[u"payload"] = payload_dict
                return funct(*args, **kwargs)
            else:
                return flask_constructor_error(
                    message=u"The payload format is unknown.",
                    custom_error_code=u"WRONG_PAYLOAD_FORMAT",
                    status=422
                )

        return wrapper

    return decorated


def define_before_request_function(app):
    @app.before_request
    def before_request():
        user = users.get_current_user()
        if user:
            if is_user_in_db(user):
                return
            else:
                if insert_new_user(user):
                    return
        abort(403)
