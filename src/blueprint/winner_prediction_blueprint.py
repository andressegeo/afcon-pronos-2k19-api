# -*- coding: utf-8 -*-
from flask import Blueprint, request, abort
from google.appengine.api import users
import json

import src.requests as req
from .blueprint_utils import flask_construct_response
import logging

WINNER_PREDICTION_API_BLUEPRINT = Blueprint(u'winner_prediction_api', __name__)

"""
As her name indicates, this method allow to get the winner prediction according by user
"""

"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/<int:user_id>', methods=[u'GET'])
def get_prediction_winner(user_id):
    items = req.getPredictionWinner(user_id)
    return flask_construct_response({u'items': items})

"""
"""
As her name indicates, this method allow to get the winner prediction according by user
"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_prediction_winner():
    items = req.getPredictionWinner()
    print items
    if items == 0:   
        return flask_construct_response({u'response':"Vous n'avez pas encore saisi votre prediction"})
    else:
        return flask_construct_response({u'items':items})

"""
As her name indicates, this method allow to get one prediction define by user
"""



@WINNER_PREDICTION_API_BLUEPRINT.route(u'/<int:id>', methods=[u'GET'])
def get_one_prediction(id):
    items = req.getOnePrediction()
    return flask_construct_response({u'items': items})


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

"""
@WINNER_PREDICTION_API_BLUEPRINT.route(u'/', methods=[u'POST'])
def add_winner():
    winner = json.loads(request.data).get(u'winner', None)
    items = req.addWinner(winner)
    return flask_construct_response({u'items': items})
"""


@WINNER_PREDICTION_API_BLUEPRINT.route(u'/', methods=[u'POST'])
def add_winner():

    win = json.loads(request.data)
    check = req.addWinner(win)
    #print check

    print check
    if check == 1:
        return flask_construct_response({u'response':'Insert successfull'})
    elif check == 0:
        return flask_construct_response({u'response':'Error during insertion'})
    elif check == 2:
        return flask_construct_response({u'response':'You have not right to update the prediction'})
    else:
        return flask_construct_response({u'response':'Nothing' })


