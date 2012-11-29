# -*- coding: utf-8 -*-

PROJECT = "EasyDraft"

class BaseConfig(object):

    DEBUG = True
    SECRET_KEY = 'secret key'

    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = 'easydraft'
    MYSQL_DATABASE_PASSWORD = 'easydraft_pass'
    MYSQL_DATABASE_DB = 'EasyDraft'

class ProductionConfig(BaseConfig):

    DEBUG = False
