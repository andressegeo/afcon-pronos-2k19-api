# -*- coding: utf-8 -*-
from flask import Blueprint, request, abort
from google.appengine.api import users
import json

import src.requests as req
from .blueprint_utils import flask_construct_response
import logging

WINNER_API_BLUEPRINT = Blueprint(u'winner_api', __name__)

"""
As her name indicates, this method allow to get the winner prediction according by user
"""


@WINNER_API_BLUEPRINT.route(u'/', methods=[u'GET'])
def get_winner():
    items = req.get_worldcup_winner()
    return flask_construct_response({u'winner': items})



@WINNER_API_BLUEPRINT.route(u'/', methods=[u'POST'])
def post_winner():
    # if not users.is_current_user_admin():
    #     abort(403)

    winner = json.loads(request.data)
    # print winner
    items = req.post_winner_wc(winner)
    check = req.update_point_final(winner)

    if check == 1:
        return flask_construct_response({u'response': 'Update points and score successfull'})
    else:
        return flask_construct_response({u'response': 'Error during update points'})

