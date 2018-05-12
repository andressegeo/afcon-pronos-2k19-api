import src.requests as req
import logging
from flask import Blueprint, request, json
from .blueprint_utils import flask_construct_response
USERS_API_BLUEPRINT = Blueprint(u'users_api', __name__)

Users = [
	{
        "id" : 1,
        "email":"namesgeo@gmail.com",
        "name": "Geo",
        "entity": "chepas",
        "picture_url": "htttp://chepas.sq",
        "worldcup_winner": 1,
        "points": 21
    },
    {
        "id" : 1,
        "email":"namesgeo@gmail.com",
        "name": "Geo",
        "entity": "chepas",
        "picture_url": "htttp://chepas.sq",
        "worldcup_winner": 1,
        "points": 21
    }
]


"""
As her name indicates, this method allow to get all users in database
"""
@USERS_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_all_users():
    #items = req.getAllUsers()
    return flask_construct_response({u'items':Users})


"""
As her name indicates, this method allow to retrieve current connected user and its details
"""
@USERS_API_BLUEPRINT.route(u'/me', methods=[u'GET'])
def get_me_as_user():
    #items = req.getMeAsUser()
    return flask_construct_response({u'items':Users[0]})