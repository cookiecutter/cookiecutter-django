Dokku
=====

You need to make sure you have a server running Dokku with at least 1GB of RAM. Backing services are
added just like in Heroku however you must ensure you have the relevant Dokku plugins installed.

.. code-block:: bash

    cd /var/lib/dokku/plugins
    git clone https://github.com/rlaneve/dokku-link.git link
    git clone https://github.com/luxifer/dokku-redis-plugin redis
    git clone https://github.com/jezdez/dokku-postgres-plugin postgres
    dokku plugins-install

You can specify the buildpack you wish to use by creating a file name .env containing the following.

.. code-block:: bash

    export BUILDPACK_URL=<repository>

You can then deploy by running the following commands.

..  code-block:: bash

    git remote add dokku dokku@yourservername.com:{{cookiecutter.repo_name}}
    git push dokku master
    ssh -t dokku@yourservername.com dokku redis:create {{cookiecutter.repo_name}}-redis
    ssh -t dokku@yourservername.com dokku redis:link {{cookiecutter.repo_name}}-redis {{cookiecutter.repo_name}}
    ssh -t dokku@yourservername.com dokku postgres:create {{cookiecutter.repo_name}}-postgres
    ssh -t dokku@yourservername.com dokku postgres:link {{cookiecutter.repo_name}}-postgres {{cookiecutter.repo_name}}
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_SETTINGS_MODULE='config.settings.production'
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY
    ssh -t dokku@yourservername.com dokku config:set {{cookiecutter.repo_name}} DJANGO_MAILGUN_SERVER_NAME=YOUR_MAILGUN_SERVER
    ssh -t dokku@yourservername.com dokku run {{cookiecutter.repo_name}} python manage.py migrate
    ssh -t dokku@yourservername.com dokku run {{cookiecutter.repo_name}} python manage.py createsuperuser

When deploying via Dokku make sure you backup your database in some fashion as it is NOT done automatically.
