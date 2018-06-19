#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:5000 --chdir=/app
