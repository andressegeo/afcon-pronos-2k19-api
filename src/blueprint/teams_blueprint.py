import src.requests as req
import logging
from flask import Blueprint, request, json
from .blueprint_utils import flask_construct_response
TEAMS_API_BLUEPRINT = Blueprint(u'teams_api', __name__)



"""
As her name indicates, this method allow to get all teams in database
"""
@TEAMS_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_all_teams():
    items = req.getAllTeams()
    return flask_construct_response({u'items':items})