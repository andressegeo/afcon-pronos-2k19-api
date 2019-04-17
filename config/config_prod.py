# coding: utf-8
"""
Configuration file.
"""
import logging
import os
default_pass = u"localroot1234"

CONFIG = {
    u"db": {
        u"unix_socket": u"/cloudsql/pronos-can-2019:europe-west3:pronos-can",
        u"user": u"root",
        u"host" : u"35.246.169.22",
        u"password": u"localroot1234",
        u"database": u"preprod_afcon_2019",
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
