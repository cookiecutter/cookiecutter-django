#!/usr/bin/env bash
set -eou pipefail


main() {

# check if both the files exist
if [[ -f ./.envs/.local/.django && -f ./.envs/.local/.postgres ]]; then
    echo "Both .env files exist"

    # variables defined from now on will automatically get exported in Bourne-like shells
    set -a

    # read key=val pairs from .env files
    source ./.envs/.local/.django
    source ./.envs/.local/.postgres

    # Stop automatic variable export
    set +a

    # Mnaually create and export the DATABASE_URL
    # as it is being created and exported by the ./compose/production/django/entrypoint script
    export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

    # If REDIS_URL exists
    if [[ "${REDIS_URL-default}" != "default" ]]; then
        echo "REDIS_URL exists"
        # export CELERY_BROKER_URL
        export CELERY_BROKER_URL="${REDIS_URL}"
    fi
fi

# exporting a bash variable makes it available to all child processes in the same shell
# so any other executeable executed in the same Bash session will also get those variables
# which is what we want since we want mypy to get these
# (mypy would be a seperate exec in the current bash session for example)

mypy "$@"

}


# "$@" passes any args passed to the script (mypy.sh) to the main function
# main then passes on all those args to mypy. That is why there is a "$@" in
# the mypy exec as well.
main "$@"
