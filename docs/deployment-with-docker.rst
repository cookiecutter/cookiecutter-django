Deployment with Docker
=======================

.. index:: Docker, deployment

Prerequisites
-------------

* Docker (at least 1.10)
* Docker Compose (at least 1.6)

Understand the Compose Setup
--------------------------------

Before you start, check out the `production.yml` file in the root of this project. This is where each component
of this application gets its configuration from. Notice how it provides configuration for these services:

* `postgres` service that runs the database
* `redis` for caching
* `caddy` as webserver
* `django` is the Django project run by gunicorn

If you chose the `use_celery` option, there are two more services:

* `celeryworker` which runs the celery worker process
* `celerybeat` which runs the celery beat process

Populate .env With Your Environment Variables
---------------------------------------------

Some of these services rely on environment variables set by you. There is an `env.example` file in the
root directory of this project as a starting point. Add your own variables to the file and rename it to `.env`. This
file won't be tracked by git by default so you'll have to make sure to use some other mechanism to copy your secret if
you are relying solely on git.

It is **highly recommended** that before you build your production application, you set your POSTGRES_USER value here. This will create a non-default user for the postgres image. If you do not set this user before building the application, the default user 'postgres' will be created, and this user will not be able to create or restore backups.

To obtain logs and information about crashes in a production setup, make sure that you have access to an external Sentry instance (e.g. by creating an account with `sentry.io`_), and set the `DJANGO_SENTRY_DSN` variable. This should be enough to report crashes to Sentry.

You will probably also need to setup the Mail backend, for example by adding a `Mailgun`_ API key and a `Mailgun`_ sender domain, otherwise, the account creation view will crash and result in a 500 error when the backend attempts to send an email to the account owner.

.. _sentry.io: https://sentry.io/welcome
.. _Mailgun: https://mailgun.com

HTTPS is on by default
----------------------

SSL (Secure Sockets Layer) is a standard security technology for establishing an encrypted link between a server and a client, typically in this case, a web server (website) and a browser. Not having HTTPS means that malicious network users can sniff authentication credentials between your website and end users' browser.

It is always better to deploy a site behind HTTPS and will become crucial as the web services extend to the IoT (Internet of Things). For this reason, we have set up a number of security defaults to help make your website secure:

* In the `.env.example`, we have made it simpler for you to change the default `Django Admin` into a custom name through an environmental variable. This should make it harder to guess the access to the admin panel.

* If you are not using a subdomain of the domain name set in the project, then remember to put the your staging/production IP address in the :code:`DJANGO_ALLOWED_HOSTS` environment variable (see :ref:`settings`) before you deploy your website. Failure to do this will mean you will not have access to your website through the HTTP protocol.

* Access to the Django admin is set up by default to require HTTPS in production or once *live*.


HTTPS is configured by default
------------------------------

The Caddy webserver used in the default configuration will get you a valid certificate from Lets Encrypt and update it automatically. All you need to do to enable this is to make sure that your DNS records are pointing to the server Caddy runs on.

You can read more about this here at `Automatic HTTPS`_ in the Caddy docs.

.. _Automatic HTTPS: https://caddyserver.com/docs/automatic-https


Optional: Postgres Data Volume Modifications
---------------------------------------------

Postgres is saving its database files to the `postgres_data` volume by default. Change that if you want something else and make sure to make backups since this is not done automatically.

Run your app with docker-compose
--------------------------------

To get started, pull your code from source control (don't forget the `.env` file) and change to your projects root
directory.

You'll need to build the stack first. To do that, run::

    docker-compose -f production.yml build

Once this is ready, you can run it with::

    docker-compose -f production.yml up

To run a migration, open up a second terminal and run::

   docker-compose -f production.yml run django python manage.py migrate

To create a superuser, run::

   docker-compose -f production.yml run django python manage.py createsuperuser

If you need a shell, run::

   docker-compose -f production.yml run django python manage.py shell

To get an output of all running containers.

To check your logs, run::

   docker-compose -f production.yml logs

If you want to scale your application, run::

   docker-compose -f production.yml scale django=4
   docker-compose -f production.yml scale celeryworker=2

.. warning:: Don't run the scale command on postgres, celerybeat, or caddy.

If you have errors, you can always check your stack with `docker-compose`. Switch to your projects root directory and run::

    docker-compose -f production.yml ps


Supervisor Example
-------------------

Once you are ready with your initial setup, you want to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run `docker-compose -f production.yml up` in your projects root directory.

If you are using `supervisor`, you can use this file as a starting point::

    [program:{{cookiecutter.project_slug}}]
    command=docker-compose -f production.yml up
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
