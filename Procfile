web: gunicorn gambitChallenge.wsgi --log-file -
worker: celery -A gambitChallenge worker -l info
worker: celery -A gambitChallenge beat -l info
