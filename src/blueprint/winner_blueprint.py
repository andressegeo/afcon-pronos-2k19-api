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
