release: apt-get install libsm6 libxrender1 libfontconfig1 libice6
web: gunicorn -k eventlet -w 1 app:app --log-file=-
