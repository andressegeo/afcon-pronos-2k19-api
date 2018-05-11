import src.requests as req
import logging
from flask import Blueprint, request, json
from .blueprint_utils import flask_construct_response
MATCHES_API_BLUEPRINT = Blueprint(u'matches_api', __name__)



"""
As her name indicates, this method allow to retrieve the games open to prediction and the passed ones
"""
@MATCHES_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_all_matches():
    items = req.getAllMatches()
    return flask_construct_response({u'items':items})



"""
As her name indicates, this method allow to send the current user prediction for this game
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:id>/predict', methods=[u'POST'])
def predict_one_match():
    items = req.predictMatch()
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to send the game score
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:id>/enter_score', methods=[u'POST'])
def scoring_one_match():
    items = req.scoringMatch()
    return flask_construct_response({u'items':items})