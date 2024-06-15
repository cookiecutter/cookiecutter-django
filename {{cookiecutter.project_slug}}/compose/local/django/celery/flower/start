#!/bin/bash

set -o errexit
set -o nounset


until timeout 10 celery -A config.celery_app inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'


exec watchfiles --filter python celery.__main__.main \
    --args \
    "-A config.celery_app -b \"${CELERY_BROKER_URL}\" flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""
