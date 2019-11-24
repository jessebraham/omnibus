#!/bin/sh

set -e

# The `manage.py` script will use development settings by default, so make sure
# that it's loading from the production settings.
export DJANGO_SETTINGS_MODULE="omnibus.settings.production"

# Run all database migrations and collect all static files prior to running the
# application.
python manage.py migrate
python manage.py collectstatic

# Run the application using gunicorn. Increase the default timeout and set the
# thread type while we're at it.
gunicorn omnibus.wsgi -b 0.0.0.0:8000 -t 60 -k gthread
