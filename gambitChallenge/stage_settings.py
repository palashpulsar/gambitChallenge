from .settings import *

import dj_database_url

# Heroku Database (Link: https://devcenter.heroku.com/articles/django-app-configuration):
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

INSTALLED_APPS += ('storages',)
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'gambit-challenge'

# For static file
STATIC_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CELERY_BROKER_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

