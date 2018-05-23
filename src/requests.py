# coding: utf-8
#!/usr/bin/python
from google.appengine.api import users
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
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'name' : row[1],
                u'iso2' : row[2],
                u'flag_url' : row[3],
                u'eliminated' : row[4]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


"""
All the users blueprint methods [2]
"""

def get_user_connect():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        print nickname
        return nickname 
    else:
        return "idk@kestuf.com"

def getAllUsers():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'email' : row[1],
                u'name' : row[2],
                u'entity' : row[3],
                u'picture_url' : row[4],
                u'worldcup_winner': row[5],
                u'points': row[6]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items

def getMeAsUser():

    
    user = get_user_connect()
    print (user) 
    me = [] 
    table = []
    sstable = []
    #check = "andresse.njeungoue@devteamgcloud.com"
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM users where email ='"+user+"'")
        for row in cursor.fetchall():
            me.append({
                u'id': row[0],
                u'email': row[1],
                u'name': row[2],
                u'entity': row[3],
                u'picture_url': row[4],
                u'worldcup_winner': row[5],
                u'points': row[6]
            })
        
        id = str(me[0]["id"])
        table.append({u'Me':me})

        

        cursor.execute("SELECT * FROM predictions where users_id ='"+id+"'")
        for row in cursor.fetchall():
            idM = row[0]

            sstable.append({
                u'id': row[0],
                u'matches_id': row[1],
                u'score': row[2],
                u'fixture': getFixture(str(idM)),
                u'winner': row[3]              
            })
        print idM

        """
        id_match = str(sstable[0]["id"])
        print id_match
        cursor.execute("SELECT * FROM matches where id ='"+id_match+"'")
        for row in cursor.fetchall():
            sstable.append({
                u'id': row[0],
                u'match_time': row[2],
                u'team1': row[3],
                u'team2': row[4]
            })

        """
        table.append({u'predictions':sstable})
    
        con.commit()
    except TypeError as e:
        print(e)
    return table

def getTeam(id):
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams where id ='"+id+"'")
        for row in cursor.fetchall():
            team = row[1]
        return team
    except TypeError as e:
        print(e)
    return team



def getFixture(id):
    print "here"
    fixture = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM matches where id ='"+id+"'")
        for row in cursor.fetchall():
            team_1 = row[3]
            team_2 = row[4]
            print team_1
            print team_2
            fixture.append({
                u'date': row[2],
                u'team1': getTeam(str(team_1)),
                u'team2': getTeam(str(team_2))
            })
        con.commit()
    except TypeError as e:
        print(e)
    return fixture
     
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

