# coding: utf-8

# !/usr/bin/python

from datetime import datetime
import MySQLdb
import logging

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


def getAllMatches():
    pass

def infos_team(team_id):
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM teams where id = " + str(team_id) + "")
        for row in cursor.fetchall():
            print(row)
            items.append({
                u'id': row[0],
                u'name': row[1],
                u'iso2': row[2],
                u'flag_url': row[3],
                u'eliminated': 'false' if row[4] == 0 else 'true'
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
            print(row)
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
                u'id': row[0],
                u'name': row[1],
                u'opening_time': row[2],
                u'closing_time': row[3],
                u'matches': construct_matches(row[0]),
            })
        con.commit()

    except BaseException, e:
        logging.error(u'Failed to get row: {}'.format(unicode(e).encode(u'utf-8')))

    return items


def compare(a, b):
    return 1 if a > b else 99 if a == b else 2


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


def get_user_id(email):
    try:
        cursor, con = connect()
        cursor.execute("SELECT id FROM users where email ='" + email + "'")
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
        cursor.execute(req, [matches_id, score, winner, users_id])
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
        cursor.execute(req, [matches_id, score, winner, users_id])
        con.commit()
        return 1
    except BaseException, e:
        logging.error(u'Failed {}'.format(unicode(e).encode(u'utf-8')))
        return 0



def getFixture(id):
    print "here"
    fixture = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM matches where id ='" + id + "'")
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


# ################################
# Part - Ranking
# ################################

# ################################
# Part - Stadiums
# ################################


def getAllStadiums():
    items = []
    try:
        cursor, con = connect()
        cursor.execute("SELECT * FROM stadiums")
        for row in cursor.fetchall():
            print(row)
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
                u'eliminated': 'false' if row[4] == 0 else 'true'
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
        print u"Entity: " + entity
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
    for property in user_db:
        user_obj[u"id"] = property
        user_obj[u"email"] = property
        user_obj[u"name"] = property
        user_obj[u"entity"] = property
        user_obj[u"picture_url"] = property
        user_obj[u"worldcup_winner"] = property
        user_obj[u"points"] = property
        user_obj[u"is_admin"] = property

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
            # print(row)
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
        # print idM

        try:
            idM
        except NameError:
            var_exists = False
            print var_exists
        else:
            var_exists = True
        print var_exists

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
                                                                                                          int(
                                                                                                              user_admin))
        cursor.execute(query)

        con.commit()
        return get_user(user)
    except TypeError as e:
        print(e)


def addWinner(winner):
    if not winner:
        winner_id = u"NULL"
    else:
        winner_id = winner.get(u'id')

    user = get_current_user()

    cursor, con = connect()
    query = u"UPDATE users SET worldcup_winner = {} WHERE id = {}".format(winner_id, user.get(u"id"))
    cursor.execute(query)
    con.commit()


def retrieve_my_winner(user):
    if user.get(u"worldcup_winner"):
        cursor, con = connect()
        query = u"SELECT * FROM teams where id = {}".format(user.get(u"worldcup_winner"))
        cursor.execute(query)

        team = cursor.fetchone()

        my_favorite_team = {
            u"id": team[0],
            u"name": team[1],
            u"iso2": team[2],
            u"flag_url": team[3],
            u"eliminated": team[4]
        }

        user[u"worldcup_winner"] = my_favorite_team

    return user


# ################################
# Part - Predictions
# ################################


def get_prediction(prediction):
    cursor, con = connect()
    query = u"SELECT * FROM predictions where matches_id={} AND users_id={}".format(prediction.get(u'matches_id'),
                                                                                    prediction.get(u'users_id'))
    cursor.execute(query)
    return cursor.fetchone()


def update_prediction(prediction):
    cursor, con = connect()
    query = u"UPDATE predictions SET score={}, winner={} WHERE id={}".format(prediction.get(u'score'),
                                                                             prediction.get(u'winner'),
                                                                             prediction.get(u'id'))
    con.commit()
    cursor.execute(query)
    return get_prediction(prediction)


def insert_new_prediction(prediction):
    cursor, con = connect()
    query = u"INSERT INTO predictions (matches_id, score, winner, users_id) VALUES ({}, {}, {}, {})".format(
        prediction.get(u'matches_id'),
        prediction.get(u'score'),
        prediction.get(u'winner'),
        prediction.get(u'users_id')
    )
    cursor.execute(query)
    con.commit()
    return get_prediction(prediction)


def predict(prediction):
    if get_prediction(prediction):
        update_prediction(prediction)
    else:
        insert_new_prediction(prediction)
    return get_prediction(prediction)


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
            winner = getTeam(str(row[0]))
            tab.append({
                u'user': user,
                u'winner_prediction': winner
            })
        return tab
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


def post_winner_wc(winner):
    try:
        cursor, con = connect()
        cursor.execute("UPDATE worldcup SET winner=" + str(winner.get(u'id')))
        con.commit()
    except TypeError as e:
        print(e)


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
            cursor.execute("UPDATE users SET worldcup_winner =" + str(win) + " where email = '" + str(email) + "'")
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


if __name__ == '__main__':
    pass
