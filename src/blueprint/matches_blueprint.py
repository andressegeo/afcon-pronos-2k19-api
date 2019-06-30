from flask import Blueprint, request, abort, jsonify
from google.appengine.api import users
import json
import logging
import datetime

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
    # random predict all score of current user none predicted before playing the first match
    # predict = request.data
    # print predict
    logging.info('yeah')
    response = req.random_user_predict()
    return flask_construct_response({"resp":"yes"})

@MATCHES_API_BLUEPRINT.route(u'/<int:id>/predict', methods=[u'POST'])
def predict_one_match(id):
    predict = json.loads(request.data)
    print "prediction: {}".format(predict)
    date_now = datetime.datetime.now()
    # don't allow user to predict before end of game when bypass front to betting score
    a,b = predict['score'].split('-')
    a = int(a)
    b = int (b)
    if (a < 0 or a>20):
        a = 0
    if (b < 0 or b>20):
        b = 0
    predict['score'] = u'{}-{}'.format(a,b)
    # print predict

    my_predict = req.predict(id, predict)
    # print "FINPRED: {}".format(my_predict)
    return flask_construct_response(my_predict)


@MATCHES_API_BLUEPRINT.route(u'/<int:id>/enter_score', methods=[u'POST'])
def scoring_one_match(id):
    print "we here to enter_score"
    # check if current user has rights to enter score
    if not users.is_current_user_admin():
        abort(403, {'message': 'you have not rights to enter score, contact admin'})
    predict = json.loads(request.data)
    print predict
    try:
        result = req.update_points(id, predict)
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


