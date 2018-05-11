import src.requests as req
import logging
from flask import Blueprint, request, json
from .blueprint_utils import flask_construct_response
WINNER_PREDICTION_API_BLUEPRINT = Blueprint(u'winner_prediction_api', __name__)


"""
As her name indicates, this method allow to get the winner prediction according by user
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_prediction_winner():
    items = req.getPredictionWinner()
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to get one prediction define by user
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/<int:id>', methods=[u'GET'])
def get_one_prediction():
    items = req.getOnePrediction()
    return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to post by user the winner prediction of the worldcup 2k18
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/', methods=[u'POST'])
def add_winner():
    items = req.addWinner()
    return flask_construct_response({u'items':items})



