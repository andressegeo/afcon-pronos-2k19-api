from flask import Blueprint

import src.requests as req
from .blueprint_utils import flask_construct_response

STADIUMS_API_BLUEPRINT = Blueprint(u'stadiums_api', __name__)

"""
As her name indicates, this method allow to get all stadiums of the tournament
"""


@STADIUMS_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_all_stadiums():
    items = req.getAllStadiums()
    return flask_construct_response({u'items': items})
