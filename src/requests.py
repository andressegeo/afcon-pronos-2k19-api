# coding: utf-8
#!/usr/bin/python

from flask import jsonify, json
from config import CONFIG
import MySQLdb
import logging


def connect():
    con = MySQLdb.connect(
        unix_socket=CONFIG[u"db"][u"unix_socket"],
        host=CONFIG[u"db"][u"host"],
        user=CONFIG[u"db"][u"user"],
        passwd=CONFIG[u"db"][u"password"],
        db=CONFIG[u"db"][u"database"],
        charset=u"utf8",
        use_unicode=True)
    cursor = con.cursor()
    return cursor, con

"""
All the matches blueprint methods [3]
"""

def get_all_matches():
    pass



def predict_one_match():
    pass


def scoring_one_match():
    pass


"""
All the ranking blueprint methods [1]
"""
def get_ranking():
    pass


"""
All the stadiums blueprint methods [1]
"""
def get_all_stadiums():
    pass


"""
All the teams blueprint methods [1]
"""
def get_all_teams():
    pass

"""
All the users blueprint methods [2]
"""
def get_all_users():
    pass

def get_me_as_user():
    pass

"""
All the winner_prediction blueprint methods [3]
"""
def get_prediction_winner():
    pass

def get_one_prediction():
    pass

def add_winner():
    pass

if __name__ == '__main__':
    pass

