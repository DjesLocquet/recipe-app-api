#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status.

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

# Start Wsgi server as main process
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
