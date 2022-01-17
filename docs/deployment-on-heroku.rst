Deployment on Heroku
====================

.. index:: Heroku

Script
------

Run these commands to deploy the project to Heroku:

#. Create app on Heroku ::

    heroku create --buildpack heroku/python

    heroku addons:create heroku-postgresql:hobby-dev

#. Database setup

    #. Postgres
        .. code-block:: bash

            # Postgres
            # On Windows use double quotes for the time zone, e.g.
            # heroku pg:backups schedule --at "02:00 America/Los_Angeles" DATABASE_URL
            heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
            heroku pg:promote DATABASE_URL

    #. MySQL

        To add mysql to yout app when deploying it on heroku, you have to add it through some add-on that support MySQL.
        Check the full list of add-ons on `Heroku Add-ons`_. Here **JAWSDB Add-ons** is being used.

        .. code-block:: bash

            heroku addons:create jawsdb --app <name_of_your_app>
            # or
            heroku addons:create jawsdb --app <name_of_your_app> --version=<your_desired_mysql_version>

            # once database is delployed, you can run the following command to get the connection url,
            heroku config:get JAWSDB_URL
            >> mysql://username:password@hostname:port/default_schema

            # backups
            heroku addons:create jawsdb --bkpwindowstart 00:30 --bkpwindowend 01:00 --mntwindowstart Tue:23:30 --mntwindowend Wed:00:00 --app <name_of_your_app>

            # To find more about jawsdb backups
            # https://devcenter.heroku.com/articles/jawsdb#backup-import-data-from-jawsdb-or-another-mysql-database

#. Redis connection setup

    .. code-block:: bash

        heroku addons:create heroku-redis:hobby-dev

#. Mailgun

    .. code-block:: bash

        # Assuming you chose Mailgun as mail service (see below for others)
        heroku addons:create mailgun:starter

#. Setting up environment variables

.. code-block:: bash

        heroku config:set PYTHONHASHSEED=random

        heroku config:set WEB_CONCURRENCY=4

        heroku config:set DJANGO_DEBUG=False
        heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
        heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"

        # Generating a 32 character-long random string without any of the visually similar characters "IOl01":
        heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"

        # Set this to your Heroku app url, e.g. 'bionic-beaver-28392.herokuapp.com'
        heroku config:set DJANGO_ALLOWED_HOSTS=

        # Assign with AWS_ACCESS_KEY_ID
        heroku config:set DJANGO_AWS_ACCESS_KEY_ID=

        # Assign with AWS_SECRET_ACCESS_KEY
        heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=

        # Assign with AWS_STORAGE_BUCKET_NAME
        heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=

#. Deploying

    .. code-block:: bash

        git push heroku master

        heroku run python manage.py createsuperuser

        heroku run python manage.py check --deploy

        heroku open

.. _Heroku Add-ons: https://elements.heroku.com/addons

Notes
-----

Email Service
+++++++++++++

The script above assumes that you've chose Mailgun as email service. If you want to use another one, check the `documentation for django-anymail <https://anymail.readthedocs.io>`_ to know which environment variables to set. Heroku provides other `add-ons for emails <https://elements.heroku.com/addons#email-sms>`_ (e.g. Sendgrid) which can be configured with a similar one line command.

.. warning::

    .. include:: mailgun.rst

Heroku & Docker
+++++++++++++++

Although Heroku has some sort of `Docker support`_, it's not supported by cookiecutter-django.
We invite you to follow Heroku documentation about it.

.. _Docker support: https://devcenter.heroku.com/articles/build-docker-images-heroku-yml

Optional actions
----------------

Celery
++++++

Celery requires a few extra environment variables to be ready operational. Also, the worker is created,
it's in the ``Procfile``, but is turned off by default:

.. code-block:: bash

    # Set the broker URL to Redis
    heroku config:set CELERY_BROKER_URL=`heroku config:get REDIS_URL`
    # Scale dyno to 1 instance
    heroku ps:scale worker=1

Sentry
++++++

If you're opted for Sentry error tracking, you can either install it through the `Sentry add-on`_:

.. code-block:: bash

    heroku addons:create sentry:f1


Or add the DSN for your account, if you already have one:

.. code-block:: bash

    heroku config:set SENTRY_DSN=https://xxxx@sentry.io/12345

.. _Sentry add-on: https://elements.heroku.com/addons/sentry


Gulp & Bootstrap compilation
++++++++++++++++++++++++++++

If you've opted for a custom bootstrap build, you'll most likely need to setup
your app to use `multiple buildpacks`_: one for Python & one for Node.js:

.. code-block:: bash

    heroku buildpacks:add --index 1 heroku/nodejs

At time of writing, this should do the trick: during deployment,
the Heroku should run ``npm install`` and then ``npm build``,
which runs Gulp in cookiecutter-django.

If things don't work, please refer to the Heroku docs.

.. _multiple buildpacks: https://devcenter.heroku.com/articles/using-multiple-buildpacks-for-an-app
