Deployment on Heroku
====================

.. index:: Heroku

Script
------

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack heroku/python

    # Note: this is not a free plan
    heroku addons:create heroku-postgresql:essential-0

    # On Windows use double quotes for the time zone, e.g.
    # heroku pg:backups schedule --at "02:00 America/Los_Angeles" DATABASE_URL
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:mini

    # Assuming you chose Mailgun as mail service (see below for others)
    heroku addons:create mailgun:starter

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

    git push heroku main

    heroku run python manage.py createsuperuser

    heroku run python manage.py check --deploy

    heroku open

Notes
-----

Email Service
+++++++++++++

The script above assumes that you've chose Mailgun as email service. If you want to use another one, check the `documentation for django-anymail <https://anymail.readthedocs.io>`_ to know which environment variables to set. Heroku provides other `add-ons for emails <https://elements.heroku.com/addons#email-sms>`_ (e.g. Sendgrid) which can be configured with a similar one line command.

.. warning::

    .. include:: ../includes/mailgun.rst

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


Gulp or Webpack
+++++++++++++++

If you've opted for Gulp or Webpack as frontend pipeline, you'll most likely need to setup
your app to use `multiple buildpacks`_: one for Python & one for Node.js:

.. code-block:: bash

    heroku buildpacks:add --index 1 heroku/nodejs

At time of writing, this should do the trick: during deployment,
the Heroku should run ``npm install`` and then ``npm build``,
which run the SASS compilation & JS bundling.

If things don't work, please refer to the Heroku docs.

.. _multiple buildpacks: https://devcenter.heroku.com/articles/using-multiple-buildpacks-for-an-app
