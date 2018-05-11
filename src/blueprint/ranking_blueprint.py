import src.requests as req
import logging
from flask import Blueprint, request, json
from .blueprint_utils import flask_construct_response
RANKING_API_BLUEPRINT = Blueprint(u'ranking_api', __name__)


"""
As her name indicates, this method allow to get the ranking users
"""
@RANKING_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_ranking():
    items = req.Ranking()
    return flask_construct_response({u'items':items})
