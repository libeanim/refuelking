"""
=================================
Quickstart Initializer
=================================

This tool generates a configuration file and initializes a local database.
"""

import os

CONFIG_FILE_STRING = """
import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '{}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///sample.db'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class API_KEYS():
    TANKERKOENIG = '{}'

"""
os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
os.environ['DATABASE_URL'] = 'sqlite:///sample.db'

print(__doc__)
print('Hello!')
print('This script will generate a config.py file which contains the app '
      'settings. Keep this file secret.')

tk_key = input('Please enter you Tankerkoenig api key: ')
secret_key = os.urandom(24)

print('Saving configuration...')
with open('config.py', 'w') as fl:
    fl.write(CONFIG_FILE_STRING.format(secret_key, tk_key))
    fl.flush()
print('Done.')

print('Initializing database...')
from refuelking import db
db.drop_all()
db.create_all()
print('Done.')

print('\n', 'To start the webserver run the "run_debug.py" file.')
print('Goodbye')
