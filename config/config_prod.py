# coding: utf-8
"""
Configuration file.
"""
import logging
import random
import os
default_pass = u"localroot1234"

CONFIG = {
    u"db": {
        u"unix_socket": u"/cloudsql/can-2k19:europe-west1:can",
        u"user": u"root",
        u"host" : u"35.195.109.87",
        u"password": u"Namesgeo2k19",
        u"database": u"worldcup_2018",
        u"charset": u"utf-8"
    },
    u"logging": {
        u"level": logging.INFO,
        u"pattern": u'%(levelname)s - %(asctime)s : %(message)s',
        u"pattern_debug": u'[%(filename)15s::%(funcName)15s]-[l.%(lineno)3s] %(message)s'
    },
    u"app": {
        u"env": u"prod",
        u"debug": True
    }
}

def result_check(a,b):
    c = int(random.randint(0,4))
    d = int(random.randint(0,4))
    e = '{}-{}'.format(c,d)
    if c>d:
        f=a
    elif d>c:
        f=b
    elif c==d:
        f="NULL"
    else:
        pass

    return e,f

def get_all_matches():
    CONSTRUCT_ALL_MATCHES = {
        "1":[1,4, result_check(1,4)],
        "2":[2,3, result_check(2,3)],
        "3":[5,8, result_check(5,8)],
        "4":[6,7, result_check(6,7)],
        "5":[9,11, result_check(9,11)],
        "6":[10,12, result_check(10,12)],
        "7":[13,16, result_check(13,16)],
        "8":[14,15, result_check(14,15)],
        "9":[17,20, result_check(17,20)],
        "10":[18,19, result_check(18,19)],
        "11":[21,24, result_check(21,24)],
        "12":[22,23, result_check(22,23)],
        "17":[1,2, result_check(1,2)],
        "18":[3,4, result_check(3,4)],
        "19":[5,6, result_check(5,6)],
        "20":[7,8, result_check(7,8)],
        "21":[9,10, result_check(9,10)],
        "22":[12,11, result_check(12,11)],
        "23":[13,14, result_check(13,14)],
        "24":[15,16, result_check(15,16)],
        "25":[17,18, result_check(17,18)],
        "26":[19,20, result_check(19,20)],
        "27":[21,22, result_check(21,22)],
        "28":[23,24, result_check(23,24)],
        "33":[3,1, result_check(3,1)],
        "34":[4,2, result_check(4,2)],
        "35":[7,5, result_check(7,5)],
        "36":[8,6, result_check(8,6)],
        "37":[12,9, result_check(12,9)],
        "38":[11,10, result_check(11,10)],
        "39":[15,13, result_check(15,13)],
        "40":[16,14, result_check(16,14)],
        "41":[19,17, result_check(19,17)],
        "42":[20,18, result_check(20,18)],
        "43":[23,21, result_check(23,21)],
        "44":[24,22, result_check(24,22)]
    }
    return CONSTRUCT_ALL_MATCHES
