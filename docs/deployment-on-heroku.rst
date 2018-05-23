Deployment on Heroku
====================

.. index:: Heroku

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun

    heroku config:set WEB_CONCURRENCY=4
    # Generating a 32 character-long random string without any of the visually similiar characters "IOl01":
    heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"
    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"
    heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
    heroku config:set DJANGO_ALLOWED_HOSTS='.herokuapp.com'

    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE

    # This is to be set only if you're using Sentry:
    heroku config:set DJANGO_SENTRY_DSN=YOUR_SENTRY_DSN

    heroku config:set PYTHONHASHSEED=random

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open
