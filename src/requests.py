# coding: utf-8
#!/usr/bin/python
from google.appengine.api import users
from flask import jsonify, json
from config import CONFIG
from datetime import datetime
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

def infos_team(team_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams where id = "+str(team_id)+"")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'name' : row[1],
                u'iso2' : row[2],
                u'flag_url' : row[3],
                u'eliminated' : 'false' if row[4] == 0 else 'true'
            })
        con.commit()

    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))

    return items

def infos_stadium(stadium_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stadiums where id = "+str(stadium_id)+"")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'lat' : row[1],
                u'lng' : row[2],
                u'name' : row[3],
                u'city' : row[0],
            })
        con.commit()

    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
        
    return items

"""
All the matches blueprint methods [3]
"""
def construct_matches(stages_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM matches where stages_id = "+str(stages_id)+"")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'stages_id' : row[1],
                u'match_time' : row[2],
                u'team_1' : infos_team(row[3]),
                u'team_2' : infos_team(row[4]),
                u'placeholder_1' : row[5],
                u'placeholder_2' : row[6],
                u'stadiums_id' : infos_stadium(row[7]),
                u'score' : row[8],
                u'winner' : row[9]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))

    return items

def getAllMatches():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stages")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id' : row[0],
                u'name' : row[1],
                u'opening_time' : row[2],
                u'closing_time' : row[3],
                u'matches' : construct_matches(row[0]),
            })
        con.commit()

    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))

    
    return items

def compare(a, b):
    return 1 if a > b else 99 if a == b else 2

def get_user_id(email):
    try:
        cursor, con = connect()
        cursor.execute( "SELECT id FROM users where email ='"+email+"'" )    
        for row in cursor.fetchall():
            id_user = row[0]
            print id_user
        return id_user
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
        return 0


def predictMatch(id, predict):
    matches_id = id
    print u"id is: {}".format(unicode(id).encode(u'utf-8'))
    score = predict["score"]
    winner = predict["winner"]
    print u"winner is: {}".format(winner)
    user = users.get_current_user()
    email = user.email()
    print email
    users_id = get_user_id(email)
    
    try:
        cursor, con = connect()
        req = "INSERT INTO predictions(matches_id, score, winner, users_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(req, [matches_id,score, winner, users_id])
        con.commit()
        return 1
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0
    
        


def scoringMatch(id, predict):
    matches_id = id
    print u"id is: {}".format(unicode(id).encode(u'utf-8'))
    score = predict["score"]
    winner = predict["winner"]
    print u"winner is: {}".format(winner)
    user = users.get_current_user()
    email = user.email()
    print email
    users_id = get_user_id(email)
    
    try:
        cursor, con = connect()
        req = "INSERT INTO predictions(matches_id, score, winner, users_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(req, [matches_id,score, winner, users_id])
        con.commit()
        return 1
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0


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
            items.append({
                u'id' : row[0],
                u'name' : row[1],
                u'iso2' : row[2],
                u'flag_url' : row[3],
                u'eliminated' : 'false' if row[4] == 0 else 'true'
            })
        con.commit()
        return items
    except BaseException, e:
        logging.error(u'Failed : {}'.format(unicode(e).encode(u'utf-8')))
        return 0
    


"""
All the users blueprint methods [2]
"""

def check_user_exist():
    name = get_user_connect()
    try:
        cursor, con = connect()
        cursor.execute( "SELECT email FROM users where email ='"+name+"'" )    
        for row in cursor.fetchall():
            exist = row[0]
        con.commit()
        print exist
        return "exits"
    except BaseException, e:
        logging.error(u'Failed : {}'.format(unicode(e).encode(u'utf-8')))

"""
    Help to check the first connection and insert in database.
"""
def get_user_connect():
    user = users.get_current_user()
    if user:
        nickname = user.email()
        entity = nickname.split("@")[1]
        print entity
        try:
            cursor, con = connect()
            cursor.execute( "SELECT email FROM users where email ='"+nickname+"'" )    
            for row in cursor.fetchall():
                exist = row[0]
                print exist
            try:
                exist
            except NameError:
                var_exists = False
                #print var_exists
                
                req = "INSERT INTO users(email,entity) VALUES (%s,%s)"
                cursor.execute(req, [nickname,entity])
                con.commit()
            else:
                var_exists = True
            print var_exists
            
        except BaseException, e:
            logging.error(u'Failed : {}'.format(unicode(e).encode(u'utf-8')))

        return nickname
        
    else:
        return "idk@kestuf.com"

def getAllUsers():
    get_user_connect()
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            #print(row)
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

        print table

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
        #print idM

        try:
            idM
        except NameError:
            var_exists = False
            print var_exists
        else:
            var_exists = True
        print var_exists


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
    user = get_user_connect()
    print user
    tab = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT worldcup_winner FROM users where email ='"+user+"'")
        for row in cursor.fetchall():
            winner = getTeam(str(row[0]))
            tab.append({
                u'user': user,
                u'winner_prediction': winner
            })
        return tab
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0

def getOnePrediction():
    pass

def addWinner(win):
    win = win["worldcup_winner"]
    user = users.get_current_user()
    email = user.email()
    print email
    last = datetime(2018, 6, 28)
    end_last = datetime(2018, 6, 30)
    present = datetime.now()
    print present
    if present < last:
        print "true"
        print "U can modify prediction but, des pts en moins"
        try:
            cursor, con = connect()
            cursor.execute("UPDATE users SET worldcup_winner ="+str(win)+" where email = '"+str(email)+"'")
            con.commit()
            return 1
        except BaseException, e:
            logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
            return 0

    elif last < present < end_last:
        print "false"
        print "U can't modify prediction, it's close"
        try:
            cursor, con = connect()
            cursor.execute("UPDATE users SET worldcup_winner ="+str(win)+", has_modified_worldcup_winner = 1 where email = '"+str(email)+"'")
            con.commit()
            return 1
        except BaseException, e:
            logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
            return 0
    else:
        print "prohibido"
        return 2
if __name__ == '__main__':
    pass

