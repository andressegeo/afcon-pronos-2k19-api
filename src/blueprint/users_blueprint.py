from flask import Blueprint

import src.requests as req
from .blueprint_utils import flask_construct_response
from google.appengine.api import users

USERS_API_BLUEPRINT = Blueprint(u'users_api', __name__)

Users = [
    {
        "id": 1,
        "email": "namesgeo@gmail.com",
        "name": "Geo",
        "entity": "chepas",
        "picture_url": "htttp://chepas.sq",
        "afcon_winner": 1,
        "points": 21
    },
    {
        "id": 1,
        "email": "namesgeo@gmail.com",
        "name": "Geo",
        "entity": "chepas",
        "picture_url": "htttp://chepas.sq",
        "afcon_winner": 1,
        "points": 21
    }
]

"""
As her name indicates, this method allow to get all users in database
"""


@USERS_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_all_users():
    print("hello")
    items = req.getAllUsers()
    return flask_construct_response({u'items': items})


"""
As her name indicates, this method allow to retrieve current connected user and its details
"""


@USERS_API_BLUEPRINT.route(u'/me', methods=[u'GET'])
def get_me_as_user():
    user_with_predictions = req.get_me_and_my_predictions()
    # items = req.get_me()
    # print "User as me: {}".format(user_with_predictions)
    return flask_construct_response(user_with_predictions)
