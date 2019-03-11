Deployment on Heroku
====================

.. index:: Heroku

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev
    # On Windows use double quotes for the time zone, e.g.
    # heroku pg:backups schedule --at "02:00 America/Los_Angeles" DATABASE_URL
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev

    # If using mailgun:
    heroku addons:create mailgun:starter

    heroku addons:create sentry:f1

    heroku config:set PYTHONHASHSEED=random
    
    heroku config:set WEB_CONCURRENCY=4
    
    heroku config:set DJANGO_DEBUG=False
    heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"
    
    # Generating a 32 character-long random string without any of the visually similiar characters "IOl01":
    heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"
    
    # Set this to your Heroku app url, e.g. 'bionic-beaver-28392.herokuapp.com'
    heroku config:set DJANGO_ALLOWED_HOSTS=
    
    # Assign with AWS_ACCESS_KEY_ID
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=
    
    # Assign with AWS_SECRET_ACCESS_KEY
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=
    
    # Assign with AWS_STORAGE_BUCKET_NAME
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=

    git push heroku master

    heroku run python manage.py createsuperuser
    heroku run python manage.py collectstatic --no-input

    heroku run python manage.py check --deploy

    heroku open
