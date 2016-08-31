Deployment with Docker
=======================

.. index:: Docker, deployment

Prerequisites
-------------

* Docker (at least 1.10)
* Docker Compose (at least 1.6)

Understand the Compose Setup
--------------------------------

Before you start, check out the `docker-compose.yml` file in the root of this project. This is where each component
of this application gets its configuration from. Notice how it provides configuration for these services:

* `postgres` service that runs the database
* `redis` for caching
* `nginx` as reverse proxy
* `django` is the Django project run by gunicorn

If you chose the `use_celery` option, there are two more services:

* `celeryworker` which runs the celery worker process
* `celerybeat` which runs the celery beat process

If you chose the `use_letsencrypt` option, you also have:

* `certbot` which keeps your certs from letsencrypt up-to-date

Populate .env With Your Environment Variables
---------------------------------------------

Some of these services rely on environment variables set by you. There is an `env.example` file in the
root directory of this project as a starting point. Add your own variables to the file and rename it to `.env`. This
file won't be tracked by git by default so you'll have to make sure to use some other mechanism to copy your secret if
you are relying solely on git.

Optional: nginx-proxy Setup
---------------------------

By default, the application is configured to listen on all interfaces on port 80. If you want to change that, open the
`docker-compose.yml` file and replace `0.0.0.0` with your own ip.

If you are using `nginx-proxy`_ to run multiple application stacks on one host, remove the port setting entirely and add `VIRTUAL_HOST=example.com` to your env file. Here, replace example.com with the value you entered for `domain_name`.

This pass all incoming requests on `nginx-proxy`_ to the nginx service your application is using.

.. _nginx-proxy: https://github.com/jwilder/nginx-proxy

Optional: Postgres Data Volume Modifications
---------------------------------------------

Postgres is saving its database files to the `postgres_data` volume by default. Change that if you wan't
something else and make sure to make backups since this is not done automatically.

Optional: Certbot and Let's Encrypt Setup
------------------------------------------

If you chose `use_letsencrypt` and will be using certbot for https, you must do the following before running anything with docker-compose:

Replace dhparam.pem.example with a generated dhparams.pem file before running anything with docker-compose. You can generate this on ubuntu or OS X by running the following in the project root:

::

    $ openssl dhparam -out /path/to/project/compose/nginx/dhparams.pem 2048

If you would like to add additional subdomains to your certificate, you must add additional parameters to the certbot command in the `docker-compose.yml` file:

Replace:

::

    command: bash -c "sleep 6 && certbot certonly -n --standalone -d {{ cookiecutter.domain_name }} --text --agree-tos --email mjsisley@relawgo.com --server https://acme-v01.api.letsencrypt.org/directory --rsa-key-size 4096 --verbose --keep-until-expiring --standalone-supported-challenges http-01"

With:

::

    command: bash -c "sleep 6 && certbot certonly -n --standalone -d {{ cookiecutter.domain_name }} -d www.{{ cookiecutter.domain_name }} -d etc.{{ cookiecutter.domain_name }} --text --agree-tos --email {{ cookiecutter.email }} --server https://acme-v01.api.letsencrypt.org/directory --rsa-key-size 4096 --verbose --keep-until-expiring --standalone-supported-challenges http-01"

Please be cognizant of Certbot/Letsencrypt certificate requests limits when getting this set up. The provide a test server that does not count against the limit while you are getting set up.

The certbot certificates expire after 3 months.
If you would like to set up autorenewal of your certificates, the following commands can be put into a bash script:

::

    #!/bin/bash
    cd <project directory>
    docker-compose run --rm --name certbot certbot bash -c "sleep 6 && certbot certonly --standalone -d {{ cookiecutter.domain_name }} --text --agree-tos --email {{ cookiecutter.email }} --server https://acme-v01.api.letsencrypt.org/directory --rsa-key-size 4096 --verbose --keep-until-expiring --standalone-supported-challenges http-01"
    docker exec pearl_nginx_1 nginx -s reload

And then set a cronjob by running `crontab -e` and placing in it (period can be adjusted as desired)::

    0 4 * * 1 /path/to/bashscript/renew_certbot.sh

Run your app with docker-compose
--------------------------------

To get started, pull your code from source control (don't forget the `.env` file) and change to your projects root
directory.

You'll need to build the stack first. To do that, run::

    docker-compose build

Once this is ready, you can run it with::

    docker-compose up

To run a migration, open up a second terminal and run::

   docker-compose run django python manage.py migrate

To create a superuser, run::

   docker-compose run django python manage.py createsuperuser

If you need a shell, run::

   docker-compose run django python manage.py shell

To get an output of all running containers.

To check your logs, run::

   docker-compose logs

If you want to scale your application, run::

   docker-compose scale django=4
   docker-compose scale celeryworker=2

.. warning:: Don't run the scale command on postgres, celerybeat, certbot, or nginx.

If you have errors, you can always check your stack with `docker-compose`. Switch to your projects root directory and run::

    docker-compose ps


Supervisor Example
-------------------

Once you are ready with your initial setup, you wan't to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run `docker-compose up` in your projects root directory.

If you are using `supervisor`, you can use this file as a starting point::

    [program:{{cookiecutter.project_slug}}]
    command=docker-compose up
    directory=/path/to/{{cookiecutter.project_slug}}
    redirect_stderr=true
    autostart=true
    autorestart=true
    priority=10

Place it in `/etc/supervisor/conf.d/{{cookiecutter.project_slug}}.conf` and run::

    supervisorctl reread
    supervisorctl start {{cookiecutter.project_slug}}

To get the status, run::

    supervisorctl status
