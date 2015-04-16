Deploy
========

It is possible to deploy to Heroku or to your own server by using Dokku, an open source Heroku clone.

Heroku
^^^^^^

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python
    heroku addons:add heroku-postgresql:dev
    heroku addons:add pgbackups:auto-month
    heroku addons:add sendgrid:starter
    heroku addons:add memcachier:dev
    heroku pg:promote DATABASE_URL
    heroku config:set DJANGO_CONFIGURATION=Production
    heroku config:set DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE
    git push heroku master
    heroku run python {{cookiecutter.repo_name}}/manage.py migrate
    heroku run python {{cookiecutter.repo_name}}/manage.py createsuperuser
    heroku open

Dokku
^^^^^

You need to make sure you have a server running Dokku with at least 1GB of RAM. Backing services are
added just like in Heroku however you must ensure you have the relevant Dokku plugins installed.

.. code-block:: bash

    cd /var/lib/dokku/plugins
    git clone https://github.com/rlaneve/dokku-link.git link
    git clone https://github.com/jezdez/dokku-memcached-plugin memcached
    git clone https://github.com/jezdez/dokku-postgres-plugin postgres
    dokku plugins-install

You can specify the buildpack you wish to use by creating a file name .env containing the following.

.. code-block:: bash

    export BUILDPACK_URL=<repository>

You can then deploy by running the following commands.

..  code-block:: bash

    git remote add dokku dokku@yourservername.com:{{cookiecutter.repo_name}}
    git push dokku master
    ssh -t dokku@yourservername.com dokku memcached:create {{cookiecutter.repo_name}}-memcached
    ssh -t dokku@yourservername.com dokku memcached:link {{cookiecutter.repo_name}}-memcached {{cookiecutter.repo_name}}
    ssh -t dokku@yourservername.com dokku postgres:create {{cookiecutter.repo_name}}-postgres
    ssh -t dokku@yourservername.com dokku postgres:link {{cookiecutter.repo_name}}-postgres {{cookiecutter.repo_name}}
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_CONFIGURATION=Production
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} SENDGRID_USERNAME=YOUR_SENDGRID_USERNAME
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} SENDGRID_PASSWORD=YOUR_SENDGRID_PASSWORD
    ssh -t dokku@yourservername.com dokku run {{cookiecutter.repo_name}} python {{cookiecutter.repo_name}}/manage.py migrate
    ssh -t dokku@yourservername.com dokku run {{cookiecutter.repo_name}} python {{cookiecutter.repo_name}}/manage.py createsuperuser

When deploying via Dokku make sure you backup your database in some fashion as it is NOT done automatically.