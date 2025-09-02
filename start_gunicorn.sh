#!/bin/bash
source ./venv/bin/activate
exec gunicorn garden_site.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --timeout 300 \
    --log-level debug \
    --access-logfile /tmp/gunicorn_access.log \
    --error-logfile /tmp/gunicorn_error.log
