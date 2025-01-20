from .base import *

DEBUG = False

ALLOWED_HOSTS = ['tender-ambition-production.up.railway.app','flask-production-42ee8.up.railway.app','*']

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://tender-ambition-production.up.railway.app').split(',')
