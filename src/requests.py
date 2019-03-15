# coding: utf-8

# !/usr/bin/python

import MySQLdb
import logging
import time
from datetime import datetime

from flask import abort
from google.appengine.api import users

from config import CONFIG


# ################################
# Part - CONFIG
# ################################


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


# ################################
# Part - Matches
# ################################


def infos_team(team_id):
    if not team_id:
        team_id = u"null"

    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams where id = " + str(team_id) + "")
        for row in cursor.fetchall():
            items.append({
                u'id': row[0],
                u'name': row[1],
                u'iso2': row[2],
                u'flag_url': row[3],
                u'eliminated': False if row[4] == 0 else True
            })
        con.commit()

    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


def infos_stadium(stadium_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stadiums where id = " + str(stadium_id) + "")
        for row in cursor.fetchall():
            items.append({
                u'id': row[0],
                u'lat': row[1],
                u'lng': row[2],
                u'name': row[3],
                u'city': row[0],
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
        cursor.execute("SELECT * FROM matches where stages_id = " + str(stages_id) + "")
        for row in cursor.fetchall():
            items.append({
                u'id': row[0],
                u'stages_id': row[1],
                u'match_time': datetime_to_float(row[2]),
                u'team_1': infos_team(row[3]),
                u'team_2': infos_team(row[4]),
                u'placeholder_1': row[5],
                u'placeholder_2': row[6],
                u'stadiums_id': infos_stadium(row[7]),
                u'score': row[8],
                u'winner': row[9]
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
            items.append({
                u'id': row[0],
                u'name': row[1],
                u'opening_time': datetime_to_float(row[2]),
                u'closing_time': datetime_to_float(row[3]),
                u'matches': construct_matches(row[0]),
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
            cursor.execute("SELECT * FROM matches WHERE stages_id=" + str(row[0]))
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
                    u'score': row2[8],
                    u'winner': row2[9],
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


def scoringMatch(match_id, result):
    items = []
    rslt =  result.get(u'score')
    pred = result.get(u'winner')
    if pred is None:
        pred = "NULL"
    try:
        cursor, con = connect()
        query = u"UPDATE matches SET score='{}', winner={} WHERE id={}".format(str(result.get(u'score')), pred, match_id)

        cursor.execute(query)
        con.commit()

        return 1
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
        return 0


def predictMatch(id, predict):
    matches_id = id
    score = predict["score"]
    winner = predict["winner"]
    user = users.get_current_user()
    email = user.email()
    users_id = get_user_id(email)

    try:
        cursor, con = connect()
        req = "INSERT INTO predictions(matches_id, score, winner, users_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(req, [matches_id, score, winner, users_id])
        con.commit()
        return 1
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0


def get_match(match_id):
    cursor, con = connect()
    query = u"SELECT * FROM matches m join stages s on m.stages_id=s.id where m.id = {}".format(match_id)
    cursor.execute(query)
    my_match = cursor.fetchone()
    if my_match:
        stage = {
            u"id": my_match[10],
            u"name": my_match[11],
            u"opening_time": datetime_to_float(my_match[12]),
            u"closing_time": datetime_to_float(my_match[13]),
        }
        return {
            u"id": my_match[0],
            u"stages_id": my_match[1],
            u"match_time": my_match[2],
            u"team_1": my_match[3],
            u"team_2": my_match[4],
            u"placeholder_1": my_match[5],
            u"placeholder_2": my_match[6],
            u"stadiums_id": my_match[7],
            u"score": my_match[8],
            u"winner": my_match[9],
            u"stage": stage
        }
    else:
        return None


def is_match_played_today(match_id):
    match = get_match(match_id)
    if datetime.datetime.fromtimestamp(match.get(u"match_time")).strftime(u'%Y-%m-%d %H:%M:%S').date() == \
            datetime.today().date():
        return True
    else:
        return False

"""
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
        cursor.execute(req, [matches_id, score, winner, users_id])
        con.commit()
        return 1
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0
"""


def getFixture(id):
    fixture = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM matches where id ='" + id + "'")
        for row in cursor.fetchall():
            team_1 = row[3]
            team_2 = row[4]
            fixture.append({
                u'date': row[2],
                u'team1': getTeam(str(team_1)),
                u'team2': getTeam(str(team_2))
            })
        con.commit()
    except TypeError as e:
        print(e)
    return fixture


# ################################
# Part - Ranking
# ################################

def Ranking():
    items = []
    cursor, con = connect()
    query = u"SELECT * from users u left outer join teams t on u.worldcup_winner=t.id order by u.points desc, u.email "
    cursor.execute(query)
    for row in cursor.fetchall():
        team = {
            u"id": row[9],
            u"name": row[10],
            u"iso2": row[11],
            u"flag_url": row[12],
            u"eliminated": False if row[13] == 0 else True,
        }
        user = {
            u"id": row[0],
            u"email": row[1],
            u"name": row[2],
            u"entity": row[3],
            u"picture_url": row[4],
            u"worldcup_winner": team,
            u"points": row[6],
            u"is_admin": False if row[7] == 0 else True,
            u"predictions": []
        }
        items.append(user)
    return items


# ################################
# Part - Stadiums
# ################################


def getAllStadiums():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stadiums")
        for row in cursor.fetchall():
            items.append({
                u'id': row[0],
                u'lat': row[1],
                u'lng': row[2],
                u'name': row[3],
                u'city': row[4]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


# ################################
# Part - Teams
# ################################


def getAllTeams():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams")
        for row in cursor.fetchall():
            items.append({
                u'id': row[0],
                u'name': row[1],
                u'iso2': row[2],
                u'flag_url': row[3],
                u'eliminated': False if row[4] == 0 else True
            })
        con.commit()
        return items
    except BaseException, e:
        logging.error(u'Failed : {}'.format(unicode(e).encode(u'utf-8')))
        return 0


def get_team(team_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams WHERE id=" + str(team_id))
        for row in cursor.fetchall():
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


def getTeam(id):
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams where id ='" + id + "'")
        for row in cursor.fetchall():
            team = row[1]
        return team
    except TypeError as e:
        print(e)
    return team


# ################################
# Part - Users
# ################################

def get_me_and_my_predictions():
    me = get_current_user()
    me_with_predictions = retrieve_my_predictions(me)
    return me_with_predictions


def get_user_connect():
    user = users.get_current_user()
    if user:
        email = user.email()
        entity = email.split(u"@")[1]
        cursor, con = connect()
        cursor.execute(u"SELECT email FROM users where email ='{}'".format(email))
        if len(cursor.fetchall()) < 1:
            req = u"INSERT INTO users(email,entity) VALUES (%s,%s)"
            cursor.execute(req, [email, entity])
            con.commit()
        return email
    else:
        print u"WARNING -- UNKNOWN USER"
        raise Exception(u"Unkown user")


def is_user_in_db(user):
    cursor, con = connect()
    cursor.execute(u"SELECT email FROM users where email ='{}'".format(user.email()))
    if cursor.fetchone():
        return True


def get_user(user):
    user_obj = {}
    cursor, con = connect()
    query = u"SELECT * FROM users where email ='{}'".format(user.email())

    cursor.execute(query)
    user_db = cursor.fetchone()
    if user_db:
        user_obj[u"id"] = user_db[0]
        user_obj[u"email"] = user_db[1]
        user_obj[u"name"] = user_db[2]
        user_obj[u"entity"] = user_db[3]
        user_obj[u"picture_url"] = user_db[4]
        user_obj[u"worldcup_winner"] = user_db[5]
        user_obj[u"points"] = user_db[6]
        user_obj[u"has_modified_worldcup_winner"] = False if user_db[7] == 0 else True
        user_obj[u"is_admin"] = False if user_db[8] == 0 else True

    user_obj = retrieve_my_winner(user_obj)
    return user_obj


def get_current_user():
    user = users.get_current_user()
    user = get_user(user)
    if user:
        return user
    else:
        user = insert_new_user(user)
        return user


def getAllUsers():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            items.append({
                u'id': row[0],
                u'email': row[1],
                u'name': row[2],
                u'entity': row[3],
                u'picture_url': row[4],
                u'worldcup_winner': row[5],
                u'points': row[6]
            })
        con.commit()
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
    return items


def getMeAsUser():
    # user = get_user_connect()

    cursor, con = connect()

    me = [get_current_user()]
    table = []
    sstable = []
    try:
        id = str(me[0]["id"])
        table.append({u'Me': me})

        cursor.execute("SELECT * FROM predictions where users_id ='" + id + "'")
        for row in cursor.fetchall():
            idM = row[0]

            sstable.append({
                u'id': row[0],
                u'matches_id': row[1],
                u'score': row[2],
                u'fixture': getFixture(str(idM)),
                u'winner': row[3]
            })

        try:
            idM
        except NameError:
            var_exists = False
        else:
            var_exists = True

        table.append({u'predictions': sstable})

        con.commit()
    except TypeError as e:
        print(e)
    return table


def get_me():
    user = get_current_user()
    return get_user_and_predictions(user.get(u"email"))


def insert_new_user(user):
    user_email = user.email()
    user_entity = user.email().split(u"@")[1]
    user_nickname = user.nickname()
    user_admin = users.is_current_user_admin()
    try:
        cursor, con = connect()
        query = u"INSERT INTO users (email, entity, name, is_admin) VALUES ('{}', '{}', '{}', {})".format(user_email,
                                                                                                          user_entity,
                                                                                                          user_nickname,
                                                                                                          user_admin)
        cursor.execute(query)

        con.commit()
        return get_user(user)
    except TypeError as e:
        print(e)


def get_user_id(email):
    try:
        cursor, con = connect()
        cursor.execute("SELECT id FROM users where email ='" + email + "'")
        for row in cursor.fetchall():
            id_user = row[0]
        return id_user
    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))
        return 0



def addWinner(winner):
    if not winner:
        winner_id = u"NULL"
    else:
        winner_id = winner

    user = get_current_user()

    cursor, con = connect()

    query = u"UPDATE users SET worldcup_winner = {} WHERE id = {}".format(winner_id, user.get(u"id"))
    cursor.execute(query)
    con.commit()
    return winner_id



def retrieve_my_winner(user):
    if user.get(u"worldcup_winner"):
        cursor, con = connect()
        query = u"SELECT * FROM teams where id = {}".format(user.get(u"worldcup_winner"))
        cursor.execute(query)

        team = cursor.fetchone()

        if team:
            my_favorite_team = {
                u"id": team[0],
                u"name": team[1],
                u"iso2": team[2],
                u"flag_url": team[3],
                u"eliminated": False if team[4] == 0 else True
            }
        else:
            my_favorite_team = None
        user[u"worldcup_winner"] = my_favorite_team

    return user


# ################################
# Part - Predictions
# ################################


def get_prediction(prediction):
    cursor, con = connect()

    if prediction.get(u'matches_id', False) and prediction.get(u'users_id', False):

        query = u"SELECT * FROM predictions where matches_id={} AND users_id={}".format(prediction.get(u'matches_id'),
                                                                                        prediction.get(u'users_id'))
        cursor.execute(query)
        db_prediction = cursor.fetchone()
        if db_prediction:
            return {
                u"id": db_prediction[0],
                u"matches_id": db_prediction[1],
                u"score": db_prediction[2],
                u"winner": db_prediction[3],
                u"users_id": db_prediction[4]
            }

    # else if not data or not enough args to search return the given prediction (funct arg)
    return None


def update_prediction(prediction):
    pred = prediction.get(u'winner')
    if pred is None:
        pred = "NULL"
    print "my pred: {}".format(pred)
    cursor, con = connect()
    query = u"UPDATE predictions SET score='{}', winner={} WHERE id={}".format(prediction.get(u'score'),
                                                                            pred,
                                                                            prediction.get(u'id'))
    cursor.execute(query)
    con.commit()
    return get_prediction(prediction)


def insert_new_prediction(prediction):
    pred = prediction.get(u'winner')
    if pred is None:
        pred = "NULL"

    cursor, con = connect()
    query = u"INSERT INTO predictions (matches_id, score, winner, users_id) VALUES ({}, '{}', {}, {})".format(
        prediction.get(u'matches_id'),
        prediction.get(u'score'),
        pred,
        prediction.get(u'users_id')
    )

    cursor.execute(query)
    con.commit()
    
    return get_prediction(prediction)


def predict(match_id, prediction):
    try:
        user = get_current_user()
        if prediction_allowed(match_id):
            new_prediction = {
                u"id": None,
                u"matches_id": match_id,
                u"score": prediction.get(u"score"),
                u"winner": prediction.get(u"winner"),
                u"users_id": user.get(u"id")
            }

            db_prediction = get_prediction(new_prediction)
            
            # if prediction already in db
            if db_prediction:
                new_prediction[u"id"] = db_prediction.get(u"id")
                my_prediction = update_prediction(new_prediction)
            else:
                my_prediction = insert_new_prediction(new_prediction)

            return my_prediction
        else:
            abort(403)
    except BaseException, e:
        logging.error(u'Failed: {}'.format(unicode(e).encode(u'utf-8')))



def datetime_to_float(d):
    try:
        epoch = datetime.utcfromtimestamp(0)
        total_seconds = (d - epoch).total_seconds()
        # total_seconds will be in decimals (millisecond precision)
        return total_seconds
    except:
        return d


def prediction_allowed(match_id):
    if CONFIG[u"app"].get(u"debug"):
        return True
    else:
        now = time.time()
        match = get_match(match_id)
        if match:
            stage = match.get(u"stage")
            if now < stage.get(u"opening_time"):
                return False
            else:
                if stage.get(u"closing_time", False):
                    if now > stage.get(u"closing_time"):
                        return False
                    else:
                        return True
                else:
                    if is_match_played_today(match_id):
                        return False
                    else:
                        return True
        else:
            return False



"""
def predictMatch(prediction):
    items = []
    try:
        print prediction
        cursor, con = connect()
        cursor.execute(
            "SELECT * FROM predictions where matches_id=" + str(prediction.get(u'matches_id')) + " AND users_id=" + str(
                prediction.get(u'users_id')))
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
"""


def get_user_and_predictions(user_email):
    #  user = get_user_connect()
    table = []
    sstable = []
    me = []
    # check = "andresse.njeungoue@devteamgcloud.com"
    try:
        cursor, con = connect()
        cursor.execute(u"SELECT * FROM users where email ='{}'".format(user_email))
        user_db = cursor.fetchall()
        print "select boolean is_admin on db {}".format(row[7])
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


def get_all_predictions(user_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM predictions where users_id =" + str(user_id))
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


def getPredictionWinner():
    user = get_user_connect()
    print user
    tab = []
    try:
        cursor, con = connect()
        cursor.execute(u"SELECT worldcup_winner FROM users where email ='{}'".format(user))
        for row in cursor.fetchall():
            #winner = getTeam(str(row[0]))
            tab.append({
                u'user': user,
                u'winner_prediction': row[0]
            })
        return tab[0]
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0


def retrieve_my_predictions(user):
    user[u"predictions"] = []

    cursor, con = connect()
    query = u"SELECT * FROM predictions where users_id ={}".format(user.get(u"id"))
    cursor.execute(query)

    for row in cursor.fetchall():
        prediction = {
            u"id": row[0],
            u"matches_id": row[1],
            u"score": row[2],
            u"winner": row[3]
        }

        user[u"predictions"].append(prediction)

    return user


# ################################
# Part - WorldCup
# ################################


def get_worldcup_winner():
        cursor, con = connect()
        query = u"SELECT * FROM worldcup"
        cursor.execute(query)

        winner = cursor.fetchone()
        result = {
            u"winner_id": winner[0],
            u"opening_time": datetime_to_float(winner[1]),
            u"closing_time": datetime_to_float(winner[2]),
            u"flag_url": winner[3]
        }
        return result


def post_winner_wc(winner):
    print winner.get(u'flag_url')
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM worldcup")
        if cursor.fetchone():
            print "here"
            start = datetime.utcfromtimestamp(1561604614).strftime('%Y-%m-%d %H:%M:%S')
            end = datetime.utcfromtimestamp(1583938973).strftime('%Y-%m-%d %H:%M:%S')
            query = u"UPDATE worldcup SET flag_url={}, winner={}, opening_time='{}', closing_time='{}'".format("NULL", "NULL", start, end)
            # query = u"UPDATE worldcup SET flag_url='{}', winner='{}'".format("NULL", "NULL")
            # print query
            cursor.execute(query)
            # cursor.execute("UPDATE worldcup SET winner=" + str(winner['winner']))
            con.commit()
        else:
            print "here"
            req = "INSERT into worldcup(winner) VALUES (%s)"
            cursor.execute(req, [winner[u"winner"]])
            con.commit()
    except TypeError as e:
        print(e)

"""
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
        print "Vous avez modifiez avant la date de cloture de phase de poules"
        try:
            cursor, con = connect()
            cursor.execute("UPDATE users SET worldcup_winner =" + str(win) + " where email = '" + str(email) + "'")
            con.commit()
            return 1
        except BaseException, e:
            logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
            return 0

    elif last < present < end_last:
        print "Vous avez modifié durant la phase d'entre 2 tours, vous aurez des points en moins "
        try:
            cursor, con = connect()
            cursor.execute("UPDATE users SET worldcup_winner =" + str(
                win) + ", has_modified_worldcup_winner = 1 where email = '" + str(email) + "'")
            con.commit()
            return 1
        except BaseException, e:
            logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
            return 0
    else:
        print "prohibido"
        return 2
"""
def check_stages(match_id):
    
    try:
        cursor, con = connect()
        query = u"SELECT stages_id FROM matches where id ='{}'".format(match_id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            stages_id = result[0]
            return stages_id
        else:
            return 99
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 100


def get_user_points(user_id):
    
    try: 
        cursor, con = connect()
        query = u"SELECT points FROM users where id ='{}'".format(user_id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            points = result[0]
            return points
        else:
            return 109
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 209
        

def update_score(match_id, predict):
    stages_id = check_stages(match_id)
    score_final = predict.get(u'score')
    winner_final = predict.get(u'winner')
    if stages_id < 9:
        cursor, con = connect()
        cursor.execute("SELECT * FROM predictions where matches_id ='" + str(match_id) + "'")
        for row in cursor.fetchall():
            users_id = row[4]
            points = get_user_points(users_id)
            if row[2] == score_final:
                points = points + 3 
            if row[3] is None and winner_final == "NULL":
                points = points + 1 
            elif row[3] == winner_final:
                points = points + 1 
            else:
                pass
        
            try: 
                cursor, con = connect()
                query = u"UPDATE users SET points={} WHERE id={}".format(points, users_id)

                cursor.execute(query)
                con.commit()
                
            except BaseException, e:
                logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 1

    elif 9 <= stages_id <=13:
        cursor, con = connect()
        cursor.execute("SELECT * FROM predictions where matches_id ='" + str(match_id) + "'")
        for row in cursor.fetchall():
            users_id = row[4]
            points = get_user_points(users_id)
            if row[2] == score_final:
                points = points + 3 
            if row[3] is None and winner_final == "NULL":
                points = points + 1 
            elif row[3] == winner_final:
                points = points + 1 
            else:
                pass
        
            try: 
                cursor, con = connect()
                query = u"UPDATE users SET points={} WHERE id={}".format(points, users_id)
                cursor.execute(query)
                con.commit()
                
            except BaseException, e:
                logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 1
 
    
    else:
        return 2
"""
    Update users points when admin enter final winner of the worldcup at the end of tournament.
"""
def update_point_final(winner):
    win = winner['winner']
    try: 
        cursor, con = connect()
        query = u"SELECT id, worldcup_winner, points, has_modified_worldcup_winner FROM users"
        cursor.execute(query)
        for row in cursor.fetchall():
            if row[1] == win and row[3] == 0:
                points = row[2] + 15
                cursor, con = connect()
                query = u"UPDATE users SET points={} WHERE id={}".format(points, row[0])

                cursor.execute(query)
                con.commit()
                rslt = 1
            elif row[1] == win and row[3] == 1:
                points = row[2] + 10
                cursor, con = connect()
                query = u"UPDATE users SET points={} WHERE id={}".format(points, row[0])
                cursor.execute(query)
                con.commit()
                rslt = 1
            else:
                rslt = 1

        return rslt
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0




if __name__ == '__main__':
    pass
