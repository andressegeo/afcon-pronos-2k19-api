# coding: utf-8
from flask import Flask

from config import CONFIG
from src.utils import init_logger
from src.blueprint import (USERS_API_BLUEPRINT, TEAMS_API_BLUEPRINT, MATCHES_API_BLUEPRINT, WINNER_PREDICTION_API_BLUEPRINT, RANKING_API_BLUEPRINT, STADIUMS_API_BLUEPRINT  )

import MySQLdb
import src.requests as req

logging_config = CONFIG[u"logging"]
init_logger(logging_config[u'pattern'], logging_config[u'pattern_debug'], logging_config[u"level"])


# create flask server
APP = Flask(__name__)
APP.debug = CONFIG[u"app"][u"debug"]
APP.register_blueprint(USERS_API_BLUEPRINT, url_prefix = u'/users')
APP.register_blueprint(TEAMS_API_BLUEPRINT, url_prefix = u'/teams')
APP.register_blueprint(MATCHES_API_BLUEPRINT, url_prefix = u'/matches')
APP.register_blueprint(WINNER_PREDICTION_API_BLUEPRINT, url_prefix = u'/winner_prediction')
APP.register_blueprint(RANKING_API_BLUEPRINT, url_prefix = u'/ranking')
APP.register_blueprint(STADIUMS_API_BLUEPRINT, url_prefix = u'/stadiums')


if __name__ == u"__main__":
    APP.run(threaded=True, port=5000, debug=True)