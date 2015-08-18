#!/bin/bash
set -e
# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.
export DJANGO_CACHE_URL=redis://redis:6379/0

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$POSTGRES_ENV_POSTGRES_USER" ]; then
    export POSTGRES_ENV_POSTGRES_USER=postgres
fi 

export DATABASE_URL=postgres://$POSTGRES_ENV_POSTGRES_USER:$POSTGRES_ENV_POSTGRES_PASSWORD@postgres:5432/$POSTGRES_ENV_POSTGRES_USER
{% if cookiecutter.use_celery == 'y' %}
export CELERY_BROKER_URL=$DJANGO_CACHE_URL
{% endif %}
exec "$@"