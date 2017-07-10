============================
Database Backups with Docker
============================

The database has to be running to create/restore a backup. These examples show local examples. If you want to use it on a remote server, remove ``-f local.yml`` from each example.

Running Backups
================

Run the app with `docker-compose -f local.yml up`.

To create a backup, run::

    docker-compose -f local.yml run postgres backup


To list backups, run::

    docker-compose -f local.yml run postgres list-backups


To restore a backup, run::

    docker-compose -f local.yml run postgres restore filename.sql

Where <containerId> is the ID of the Postgres container. To get it, run::

    docker ps

To copy the files from the running Postgres container to the host system::

    docker cp <containerId>:/backups /host/path/target

Restoring From Backups
======================

To restore the production database to a local PostgreSQL database::

    createdb NAME_OF_DATABASE
    psql NAME_OF_DATABASE < NAME_OF_BACKUP_FILE
