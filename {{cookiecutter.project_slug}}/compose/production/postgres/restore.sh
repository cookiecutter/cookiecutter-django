#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "$POSTGRES_USER" == "postgres" ]
then
    echo "restoring as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=$POSTGRES_PASSWORD

# check that we have an argument for a filename candidate
if [[ $# -eq 0 ]] ; then
    echo 'usage:'
    echo '    docker-compose -f production.yml run postgres restore <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    docker-compose -f production.yml run postgres list-backups'
    exit 1
fi

# set the backupfile variable
BACKUPFILE=/backups/$1

# check that the file exists
if ! [ -f $BACKUPFILE ]; then
    echo "backup file not found"
    echo 'to get a list of available backups, run:'
    echo '    docker-compose -f production.yml run postgres list-backups'
    exit 1
fi

echo "beginning restore from $1"
echo "-------------------------"

# delete the db
# deleting the db can fail. Spit out a comment if this happens but continue since the db
# is created in the next step
echo "deleting old database $POSTGRES_USER"
if dropdb -h postgres -U $POSTGRES_USER $POSTGRES_USER
then echo "deleted $POSTGRES_USER database"
else echo "database $POSTGRES_USER does not exist, continue"
fi

# create a new database
echo "creating new database $POSTGRES_USER"
createdb -h postgres -U $POSTGRES_USER $POSTGRES_USER -O $POSTGRES_USER

# restore the database
echo "restoring database $POSTGRES_USER"
gunzip -c $BACKUPFILE | psql -h postgres -U $POSTGRES_USER
