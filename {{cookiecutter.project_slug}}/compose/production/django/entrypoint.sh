#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


cmd="$@"

# N.B. If only .env files supported variable expansion...
export CELERY_BROKER_URL="${REDIS_URL}"

if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}"

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="postgres"
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}

until postgres_ready; do
  >&2 echo 'PostgreSQL is unavailable (sleeping)...'
  sleep 1
done

>&2 echo 'PostgreSQL is up - continuing...'

exec $cmd
