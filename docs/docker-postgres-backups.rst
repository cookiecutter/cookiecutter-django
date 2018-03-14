PostgreSQL Backups with Docker
==============================

Prerequisites:

#. the project was generated with ``use_docker`` set to ``y``.

For brevity it is assumed that will be running the below commands against local environment, however, this is by no means mandatory so feel free switching to ``production.yml`` when needed.

Note that the application stack should not necessarily be running when applying any of the instructions below, unless explicitly stated otherwise. For instance, suppose the stack has been down for quite some time or have never even been up yet -- rather than starting it beforehand use a single ``$ docker-compose -f local.yml run --rm <command>`` with the desired command. By contrast, should you already have your application up and running do not bother waiting for ``run`` instruction to finish (they usually take a bit longer due to bootstrapping phase), just use ``$ docker-compose -f local.yml exec <command>`` instead; note that any ``exec`` command fails unless all of the required containers are running. From now on, we will be using ``run``-style examples for general-case compatibility.


Creating a Backup
-----------------

To create a backup, run::

    $ docker-compose -f local.yml run --rm postgres backup

Assuming your project's database is named ``my_project`` here is what you will see: ::

    Backing up the 'my_project' database...
    SUCCESS: 'my_project' database backup 'backup_2018_03_13T09_05_07.sql.gz' has been created and placed in '/backups'.

Keep in mind that ``/backups`` is the ``postgres`` container directory.


Viewing the Existing Backups
----------------------------

To list existing backups, ::

    $ docker-compose -f local.yml run --rm postgres backups

These are the sample contents of ``/backups``: ::

    These are the backups you have got:
    total 24K
    -rw-r--r-- 1 root root 5.2K Mar 13 09:05 backup_2018_03_13T09_05_07.sql.gz
    -rw-r--r-- 1 root root 5.2K Mar 12 21:13 backup_2018_03_12T21_13_03.sql.gz
    -rw-r--r-- 1 root root 5.2K Mar 12 21:12 backup_2018_03_12T21_12_58.sql.gz


Copying Backups Locally
-----------------------

If you want to copy backups from your ``postgres`` container locally, ``docker cp`` command_ will help you on that.

For example, given ``9c5c3f055843`` is the container ID copying all the backups over to a local directory is as simple as ::

    $ docker cp 9c5c3f055843:/backups ./backups

With a single backup file copied to ``.`` that would be ::

    $ docker cp 9c5c3f055843:/backups/backup_2018_03_13T09_05_07.sql.gz .

.. _`command`: https://docs.docker.com/engine/reference/commandline/cp/


Restoring from the Existing Backup
----------------------------------

To restore from one of the backups you have already got (take the ``backup_2018_03_13T09_05_07.sql.gz`` for example), ::

    $ docker-compose -f local.yml run --rm postgres restore backup_2018_03_13T09_05_07.sql.gz

You will see something like ::

    Restoring the 'my_project' database from the '/backups/backup_2018_03_13T09_05_07.sql.gz' backup...
    INFO: Dropping all connections to the database...
     pg_terminate_backend
    ----------------------
    (0 rows)

    INFO: Dropping the database...
    INFO: Creating a new database...
    INFO: Applying the backup to the new database...
    SET
    SET
    SET
    SET
    SET
     set_config
    ------------

    (1 row)

    SET
    # ...
    ALTER TABLE
    SUCCESS: The 'my_project' database has been restored from the '/backups/backup_2018_03_13T09_05_07.sql.gz' backup.
