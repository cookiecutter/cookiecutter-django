#!/bin/sh
su -m django -c "python /app/manage.py collectstatic --noinput"
su -m django -c "/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app"