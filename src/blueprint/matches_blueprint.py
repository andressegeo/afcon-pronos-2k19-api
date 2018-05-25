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
    items = req.get_stages_and_matches()
    print items
    return flask_construct_response({u'items':items})



"""
As her name indicates, this method allow to send the current user prediction for this game
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:match_id>/predict', methods=[u'POST'])
def predict_one_match(match_id):
    prediction = request.get_json().get(u'prediction')
    items = req.predictMatch(prediction)
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to send the game score
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:match_id>/enter_score', methods=[u'POST'])
def scoring_one_match(match_id):
    result = request.get_json().get(u'result')
    items = req.scoringMatch(match_id, result)
    return flask_construct_response({u'items':items})