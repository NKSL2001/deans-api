#!/bin/bash
cd $DJANGO_ROOT
echo 1;
python3 manage.py collectstatic --no-input;
python3 manage.py makemigrations;
python3 manage.py migrate auth;
python3 manage.py migrate;
python3 manage.py makemigrations api;
python3 manage.py migrate api;
python3 manage.py loaddata $DATA_ROOT/users.json
if [ "$PRODUCTION" -eq "1" ];
then
    gunicorn  --log-level=debug --bind :8000 deans_api.wsgi:application;
else
    python3 manage.py runserver 0.0.0.0:8000;
fi

