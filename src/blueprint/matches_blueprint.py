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
    print items
    return flask_construct_response({u'items':items})



"""
As her name indicates, this method allow to send the current user prediction for this game
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:id>/predict', methods=[u'POST'])
def predict_one_match(id):
    try:
        predict = json.loads(request.data)
        check = req.predictMatch(id, predict)

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

    #return flask_construct_response({u'items':items})


"""
As her name indicates, this method allow to send the game score by admin
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:id>/enter_score', methods=[u'POST'])
def scoring_one_match(id):
    try:
        score = json.loads(request.data)
        check = req.scoringMatch(id, predict)

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
    
    #return flask_construct_response({u'items':items})