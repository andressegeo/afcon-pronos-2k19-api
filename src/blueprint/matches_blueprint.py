from flask import Blueprint, request, abort
from google.appengine.api import users
import json
import logging

import src.requests as req
from .blueprint_utils import flask_construct_response

MATCHES_API_BLUEPRINT = Blueprint(u'matches_api', __name__)

"""
As her name indicates, this method allow to retrieve the games open to prediction and the passed ones
"""


@MATCHES_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_all_matches():
    items = req.getAllMatches()
    # logging.warn("fEds: {}".format(items))
    return flask_construct_response({u'items': items})

@MATCHES_API_BLUEPRINT.route(u'/random_predict', methods=[u'POST'])
def random_predict():
    # random predict all score of current user none predicted
    # predict = request.data
    # print predict
    return flask_construct_response({"check":"test"})

@MATCHES_API_BLUEPRINT.route(u'/<int:id>/predict', methods=[u'POST'])
def predict_one_match(id):
    predict = json.loads(request.data)
    my_predict = req.predict(id, predict)
    return flask_construct_response(my_predict)

"""
As her name indicates, this method allow to send the current user prediction for this game
"""

"""
@MATCHES_API_BLUEPRINT.route(u'/<int:id>/predict', methods=[u'POST'])
def predict_one_match(id):
    try:
        predict = json.loads(request.data)
        check = req.predict(id, predict)

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



"""
"""
@MATCHES_API_BLUEPRINT.route(u'/<int:match_id>/enter_score', methods=[u'POST'])
def scoring_one_match(match_id):
    if not users.is_current_user_admin():
        abort(403)

    result = request.get_json().get(u'result')
    items = req.scoringMatch(match_id, result)
    return flask_construct_response({u'items': items})
"""


@MATCHES_API_BLUEPRINT.route(u'/<int:id>/enter_score', methods=[u'POST'])
def scoring_one_match(id):

    # if not users.is_current_user_admin():
    #     abort(403)
    predict = json.loads(request.data)
    print predict
    try:
                
        result = req.update_score(id, predict)
        check = req.scoringMatch(id, predict)
#A revoir
        if result == 1 and check == 1:
            return flask_construct_response({u'response': 'Update points and score successfull'})
        elif result == 0 or check == 0:
            return flask_construct_response({u'response': 'Error during update points'})
        else:
            return flask_construct_response({u'response': 'Error!!!'})


    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return "Error"


