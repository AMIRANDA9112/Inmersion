web: gunicorn -k eventlet -w 1 app:app --log-file=-
worker: celery worker --app=app.celery
run: service redis-server start
