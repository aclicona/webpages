#!/bin/bash

case $1 in
  dev)
    python manage.py collectstatic --noinput
    python manage.py runserver
    ;;
  prod)
  	python manage.py collectstatic --noinput
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ;;
  celery)
    celery -A backend.celery worker --loglevel=INFO
esac