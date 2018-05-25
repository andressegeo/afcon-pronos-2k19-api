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


def get_stages_and_matches():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stages")
        results_stages = cursor.fetchall()
        for row in results_stages:
            matches = []
            stadium = {}
            cursor.execute("SELECT * FROM matches WHERE stages_id="+str(row[0]))
            results_matches = cursor.fetchall()
            for row2 in results_matches:
                cursor.execute("SELECT * FROM stadiums WHERE id=" + str(row2[7]))
                stadium = {}
                for row3 in cursor.fetchall():
                    stadium = {
                        u'id': row3[0],
                        u'lat': row3[1],
                        u'lng': row3[2],
                        u'name': row3[3],
                        u'city': row3[4]
                    }
                matches.append({
                    u'id': row2[0],
                    u'stages_id': row2[1],
                    u'match_time': row2[2],
                    u'team_1': row2[3],
                    u'team_2': row2[3],
                    u'placeholder_1': row2[4],
                    u'placeholder_2': row2[5],
                    u'stadiums_id': row2[6],
                    u'score': row2[7],
                    u'winner': row2[8],
                    u'stadium': stadium
                })
            items.append({
                u'id': row[0],
                u'name': row[1],
                u'opening_time': row[2],
                u'closing_time': row[3],
                u'matches': matches
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items



def predictMatch(prediction):
    items = []
    try:
        print prediction
        cursor, con = connect()
        cursor.execute("SELECT * FROM predictions where matches_id=" + str(prediction.get(u'matches_id')) + " AND users_id=" + str(prediction.get(u'users_id')))
        result = cursor.fetchall()
        if prediction.get(u'winner') is not None:
            prediction[u'winner'] = str(prediction[u'winner'])
        if len(result) > 0:
            cursor.execute("UPDATE predictions SET score=%s, winner=%s WHERE id=%s",
                           (prediction.get(u'score'),
                            prediction.get(u'winner'),
                            result[0][0]
                            ))
        else:
            cursor.execute("INSERT INTO predictions (matches_id, score, winner, users_id) VALUES (%s, %s, %s, %s)",
                           (str(prediction.get(u'matches_id')),
                            prediction.get(u'score'),
                            prediction.get(u'winner'),
                            str(prediction.get(u'users_id'))))
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


def scoringMatch(match_id, result):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("UPDATE matches SET score=%s, winner=%s WHERE id=%s",
                       (result.get(u'score'),
                        result.get(u'winner'),
                        match_id
                        ))
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


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


def get_team(team_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams WHERE id="+str(team_id))
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
        ret_user = {
            u'email': user.email(),
            u'name': user.email(),
            u'entity': user.email().split('@')[1]
        }
        print ret_user
        return ret_user
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

        table.append({u'predictions':sstable})

        con.commit()
    except TypeError as e:
        print(e)
    return table


def get_me():
    user = get_user_connect()
    print (user)
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM users where email ='"+user.get(u'email')+"'")
        result = cursor.fetchall()
        print 'HERE RESULT OF USER'
        if len(result) == 0:
            insert_new_user(user)
        return get_user_and_predictions(user)
    except TypeError as e:
        print(e)


def insert_new_user(user):
    try:
        cursor, con = connect()
        cursor.execute("INSERT INTO users (email, entity, name, is_admin) VALUES (%s, %s, %s, %s)",
                       (user.get(u'email'),
                        user.get(u'entity'),
                        user.get(u'name'), False))
        con.commit()
    except TypeError as e:
        print(e)


def get_user_and_predictions(user):
    table = []
    sstable = []
    me = []
    # check = "andresse.njeungoue@devteamgcloud.com"
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM users where email ='" + user.get(u'email') + "'")
        user_db = cursor.fetchall()
        if len(user_db) > 0:
            for row in user_db:
                me.append({
                    u'id': row[0],
                    u'email': row[1],
                    u'name': row[2],
                    u'entity': row[3],
                    u'picture_url': row[4],
                    u'worldcup_winner': row[5],
                    u'points': row[6],
                    u'is_admin': row[7],
                })
            id = str(me[0]["id"])
            table.append({u'Me': me})

            cursor.execute("SELECT * FROM predictions where users_id ='" + str(id) + "'")
            for row in cursor.fetchall():
                idM = row[0]
                sstable.append({
                    u'id': row[0],
                    u'matches_id': row[1],
                    u'score': row[2],
                    u'fixture': getFixture(str(idM)),
                    u'winner': row[3]
                })

            table.append({u'predictions': sstable})
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


def get_all_predictions(user_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM predictions where users_id ="+str(user_id))
        for row in cursor.fetchall():
            items.append({
                u"id": row[0],
                u"matches_id": row[1],
                u"score": row[2],
                u"winner": row[3],
                u"users_id": row[4]
            })
    except TypeError as e:
        print(e)
    return items


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
def getPredictionWinner(user_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT t.id, t.name, t.iso2, t.flag_url, t.eliminated FROM teams t JOIN users u ON u.worldcup_winner = t.id WHERE u.id=" + str(user_id))
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id': row[0],
                u'name': row[1],
                u'iso2': row[2],
                u'flag_url': row[3],
                u'eliminated': row[4]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


def getOnePrediction():
    pass

def addWinner(winner, user):
    try:
        cursor, con = connect()
        cursor.execute("UPDATE users SET worldcup_winner=" + str(winner.get(u'id')) + " WHERE id='" + str(user.get(u'id')) + "'")
        con.commit()
    except TypeError as e:
        print(e)


def post_winner_wc(winner):
    try:
        cursor, con = connect()
        cursor.execute("UPDATE worldcup SET winner=" + str(winner.get(u'id')))
        con.commit()
    except TypeError as e:
        print(e)

if __name__ == '__main__':
    pass

