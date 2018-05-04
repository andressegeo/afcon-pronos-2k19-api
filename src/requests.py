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



if __name__ == '__main__':
    pass

