import src.requests as req
import logging
from flask import Blueprint, request, json
from .blueprint_utils import flask_construct_response
WINNER_PREDICTION_API_BLUEPRINT = Blueprint(u'winner_prediction_api', __name__)


"""
As her name indicates, this method allow to get the winner prediction according by user
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/<int:user_id>', methods=[u'GET'])
def get_prediction_winner(user_id):
    items = req.getPredictionWinner(user_id)
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to get one prediction define by user
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/<int:id>', methods=[u'GET'])
def get_one_prediction(id):
    items = req.getOnePrediction()
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to get one prediction define by user
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'get_all_predictions/<int:id>', methods=[u'GET'])
def get_all_prediction(user_id):
    items = req.get_all_predictions(user_id)
    return flask_construct_response({u'items': items})


"""
As her name indicates, this method allow to post by user the winner prediction of the worldcup 2k18
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/', methods=[u'POST'])
def add_winner():
    winner = request.get_json().get(u'winner')
    user = request.get_json().get(u'user')
    items = req.addWinner(winner, user)
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to post by user the winner prediction of the worldcup 2k18
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/winner_is', methods=[u'POST'])
def post_winner():
    winner = request.get_json().get(u'winner')
    items = req.post_winner_wc(winner)
    return flask_construct_response({u'items':items})


