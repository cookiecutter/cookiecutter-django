#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

wait-for-it "${POSTGRES_HOST}:${POSTGRES_PORT}" -t 30

>&2 echo 'PostgreSQL is available'

exec "$@"
