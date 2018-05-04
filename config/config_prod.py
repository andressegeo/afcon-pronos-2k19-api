# coding: utf-8
"""
Configuration file.
"""
import logging


CONFIG = {
    u"db": {
        u"unix_socket": u"/cloudsql/",
        u"user": u"root",
        u"host" : u"",
        u"password": u"",
        u"database": u"",
        u"charset": u"utf-8"
    },
    u"logging": {
        u"level": logging.INFO,
        u"pattern": u'%(levelname)s - %(asctime)s : %(message)s',
        u"pattern_debug": u'[%(filename)15s::%(funcName)15s]-[l.%(lineno)3s] %(message)s'
    },
    u"app": {
        u"env": u"dev",
        u"debug": True
    }
}
