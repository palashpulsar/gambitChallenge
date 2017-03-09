from settings import *

import dj_database_url

# Heroku Database (Link: https://devcenter.heroku.com/articles/django-app-configuration):
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
