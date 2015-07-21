#!/bin/bash
set -e

# setting up environment variables to work with DATABASE_URL and DJANGO_CACHE_URL
export DJANGO_CACHE_URL=redis://redis:6379

if [ -z "$POSTGRES_ENV_POSTGRES_USER" ]; then
    export POSTGRES_ENV_POSTGRES_USER=postgres
fi 

export DATABASE_URL=postgres://$POSTGRES_ENV_POSTGRES_USER:$POSTGRES_ENV_POSTGRES_PASSWORD@postgres:5432/$POSTGRES_ENV_POSTGRES_USER
{% if cookiecutter.use_celery %}
export CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
{% endif %}
exec "$@"