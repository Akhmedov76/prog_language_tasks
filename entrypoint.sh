#!/bin/sh

echo "Migrating database!!!!"
python manage.py migrate

echo "Static fayllarni yigilmoqda!!!!!!"
python manage.py collectstatic --noinput

echo "Gunicorn server ishga tushmoqda!!!!!!!!!"
exec gunicorn conf.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3
