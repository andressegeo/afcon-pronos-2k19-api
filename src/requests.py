# coding: utf-8
#!/usr/bin/python

from flask import jsonify, json
from config import CONFIG
import MySQLdb
import logging


def connect():
    con = MySQLdb.connect(
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

def getAllMatches():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM matches")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'stages_id' : row[1],
                u'match_time' : row[2],
                u'team_1' : row[3],
                u'team_2' : row[4],
                u'placeholder_1' : row[5],
                u'placeholder_2' : row[6],
                u'stadiums_id' : row[7],
                u'score' : row[8],
                u'winner' : row[9]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items



def predictMatch():
    pass


def scoringMatch():
    pass


"""
All the ranking blueprint methods [1]
"""
def Ranking():
    pass


"""
All the stadiums blueprint methods [1]
"""
def getAllStadiums():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stadiums")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'lat' : row[1],
                u'lng' : row[2],
                u'name' : row[3],
                u'city' : row[4]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items



"""
All the teams blueprint methods [1]
"""
def getAllTeams():
    pass

"""
All the users blueprint methods [2]
"""
def getAllUsers():
    pass

def getMeAsUser():
    pass

"""
All the winner_prediction blueprint methods [3]
"""
def getPredictionWinner():
    pass

def getOnePrediction():
    pass

def addWinner():
    pass

if __name__ == '__main__':
    pass

