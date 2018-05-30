# coding: utf-8
from flask import Flask

from config import CONFIG
from src.utils import init_logger
from src.blueprint import (USERS_API_BLUEPRINT, TEAMS_API_BLUEPRINT, MATCHES_API_BLUEPRINT, WINNER_PREDICTION_API_BLUEPRINT,WINNER_API_BLUEPRINT, RANKING_API_BLUEPRINT, STADIUMS_API_BLUEPRINT  )
from src.blueprint.blueprint_utils import define_before_request_function, flask_constructor_error

import MySQLdb
import src.requests as req

logging_config = CONFIG[u"logging"]
init_logger(logging_config[u'pattern'], logging_config[u'pattern_debug'], logging_config[u"level"])


# create flask server
APP = Flask(__name__)
APP.debug = CONFIG[u"app"][u"debug"]
APP.register_blueprint(USERS_API_BLUEPRINT, url_prefix=u'/api/users')
APP.register_blueprint(TEAMS_API_BLUEPRINT, url_prefix=u'/api/teams')
APP.register_blueprint(MATCHES_API_BLUEPRINT, url_prefix=u'/api/matches')
APP.register_blueprint(WINNER_PREDICTION_API_BLUEPRINT, url_prefix=u'/api/winner_prediction')
APP.register_blueprint(RANKING_API_BLUEPRINT, url_prefix=u'/api/ranking')
APP.register_blueprint(STADIUMS_API_BLUEPRINT, url_prefix=u'/api/stadiums')
APP.register_blueprint(WINNER_API_BLUEPRINT, url_prefix=u'/api/winner')


# check that the user is properly logged in
define_before_request_function(APP)


@APP.errorhandler(404)
def page_not_found(e):
    return flask_constructor_error(u"Not Found", 404, 404)


@APP.errorhandler(403)
def user_forbidden(e):
    print u"forbibi"
    return flask_constructor_error(u"Forbidden", 403, 403)

if __name__ == u"__main__":
    APP.run(threaded=True, port=5000, debug=True)