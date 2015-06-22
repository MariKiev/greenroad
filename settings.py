import os
IMAGE_MAXSIZEX = 360
IMAGE_MAXSIZEY = 250

POST_PER_PAGE = 9

DB_URL = os.environ.get('DATABASE_URL')

MAIL_USERNAME = ''
MAIL_PASSWORD = ''
FLASKY_MAIL_SENDER = ''
SECRET_KEY = ''
try:
    from local_settings import *
except ImportError:
    pass
