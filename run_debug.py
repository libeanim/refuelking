#! /usr/bin/env python3
# import sys
import os
if not os.path.isfile('config.py'):
    raise SystemExit('Config file not found! Run init_all.py first.')
os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
os.environ['DATABASE_URL'] = 'sqlite:///sample.db'

from refuelking import app
# sys.path.append('.')

if __name__ == '__main__':
    print('ATTENTION! Running developement version.')
    print('APP_SETTINGS:', os.environ['APP_SETTINGS'])
    print('DATABASE_URL:', os.environ['DATABASE_URL'])
    app.run()
