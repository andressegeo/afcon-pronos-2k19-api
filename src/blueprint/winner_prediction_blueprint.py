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
    print items
    if items == 0:   
        return flask_construct_response({u'response':"Vous n'avez pas encore saisi votre prediction"})
    else:
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
    try:
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
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return "Error"



