{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}


LICENSE: BSD

Settings
------------

{{cookiecutter.project_name}} relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the '{{cookiecutter.project_name}}' environment variables to their Django setting:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_CACHES                           CACHES (default)            locmem                                         redis
DJANGO_DATABASES                        DATABASES (default)         See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
DJANGO_DEFAULT_FROM_EMAIL               DEFAULT_FROM_EMAIL          n/a                                            "{{cookiecutter.project_name}} <noreply@{{cookiecutter.domain_name}}>"
DJANGO_SERVER_EMAIL                     SERVER_EMAIL                n/a                                            "{{cookiecutter.project_name}} <noreply@{{cookiecutter.domain_name}}>"
DJANGO_EMAIL_SUBJECT_PREFIX             EMAIL_SUBJECT_PREFIX        n/a                                            "[{{cookiecutter.project_name}}] "
======================================= =========================== ============================================== ======================================================================

The following table lists settings and their defaults for third-party applications:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
{% if cookiecutter.use_sentry == "y" -%}DJANGO_SENTRY_DSN                       SENTRY_DSN                  n/a                                            raises error
DJANGO_SENTRY_CLIENT                    SENTRY_CLIENT               n/a                                            raven.contrib.django.raven_compat.DjangoClient
DJANGO_SENTRY_LOG_LEVEL                 SENTRY_LOG_LEVEL            n/a                                            logging.INFO{%- endif %}
DJANGO_MAILGUN_API_KEY                  MAILGUN_ACCESS_KEY          n/a                                            raises error
DJANGO_MAILGUN_SERVER_NAME              MAILGUN_SERVER_NAME         n/a                                            raises error
======================================= =========================== ============================================== ======================================================================

Getting up and running
----------------------

Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Create a local PostgreSQL database::

    $ createdb {{ cookiecutter.repo_name }}

Run ``migrate`` on your new database::

    $ python manage.py migrate

You can now run the ``runserver_plus`` command::

    $ python manage.py runserver_plus

Open up your browser to http://127.0.0.1:8000/ to see the site running locally.

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you'd like to take advantage of live reloading and Sass / Compass CSS compilation you can do so with a little bit of prep work.

Make sure that nodejs_ is installed. Then in the project root run::

    $ npm install

.. _nodejs: http://nodejs.org/download/

If you don't already have it, install `compass` (doesn't hurt if you run this command twice)::

    gem install compass

Now you just need::

    $ grunt serve

The base app will now run as it would with the usual ``manage.py runserver`` but with live reloading and Sass compilation enabled.

To get live reloading to work you'll probably need to install an `appropriate browser extension`_

.. _appropriate browser extension: http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-

{% if cookiecutter.use_celery == "y" %}
Celery
^^^^^^
This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd {{cookiecutter.repo_name}}
    celery -A {{cookiecutter.repo_name}}.taskapp worker -l info

Please note: For Celerys import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.
{% endif %}
{% if cookiecutter.use_maildump == "y" %}
Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For this purpose,
a Grunt task exists to start an instance of `maildump`_ which is a local SMTP server with an online interface.

.. _maildump: https://github.com/ThiefMaster/maildump

Make sure you have nodejs installed, and then type the following::

    $ grunt start-email-server

This will start an email server. The project is setup to deliver to the email server by default. To view messages
that are sent by your application, open your browser to http://127.0.0.1:1080

To stop the email server::

    $ grunt stop-email-server

The email server listens on 127.0.0.1:1025
{% endif %}
{% if cookiecutter.use_sentry == "y" %}
Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at http://getsentry.com or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
{% endif %}

It's time to write the code!!!


Running end to end integration tests
------------------------------------

N.B. The integration tests will not run on Windows.

To install the test runner::

  $ pip install hitch

To run the tests, enter the {{cookiecutter.repo_name}}/tests directory and run the following commands::

  $ hitch init

Then run the stub test::

  $ hitch test stub.test

This will download and compile python, postgres and redis and install all python requirements so the first time it runs it may take a while.

Subsequent test runs will be much quicker.

The testing framework runs Django, Celery (if enabled), Postgres, HitchSMTP (a mock SMTP server), Firefox/Selenium and Redis.


Deployment
----------

We providing tools and instructions for deploying using Docker and Heroku.

Heroku
^^^^^^

.. image:: https://www.herokucdn.com/deploy/button.png
    :target: https://heroku.com/deploy

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun

    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32`
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'

    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY

    heroku config:set PYTHONHASHSEED=random

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

Docker
^^^^^^

**Warning**

Docker is evolving extremely fast, but it has still some rough edges here and there. Compose is currently (as of version 1.4)
not considered production ready. That means you won't be able to scale to multiple servers and you won't be able to run
zero downtime deployments out of the box. Consider all this as experimental until you understand all the  implications
to run docker (with compose) on production.

**Run your app with docker-compose**

Prerequisites:

* docker (tested with 1.8)
* docker-compose (tested with 0.4)

Before you start, check out the `docker-compose.yml` file in the root of this project. This is where each component
of this application gets its configuration from. It consists of a `postgres` service that runs the database, `redis`
for caching, `nginx` as reverse proxy and last but not least the `django` application run by gunicorn.
{% if cookiecutter.use_celery == 'y' -%}
Since this application also runs Celery, there are two more services with a service called `celeryworker` that runs the
celery worker process and `celerybeat` that runs the celery beat process.
{% endif %}


All of these services except `redis` rely on environment variables set by you. There is an `env.example` file in the
root directory of this project as a starting point. Add your own variables to the file and rename it to `.env`. This
file won't be tracked by git by default so you'll have to make sure to use some other mechanism to copy your secret if
you are relying solely on git.


By default, the application is configured to listen on all interfaces on port 80. If you want to change that, open the
`docker-compose.yml` file and replace `0.0.0.0` with your own ip. If you are using `nginx-proxy`_ to run multiple
application stacks on one host, remove the port setting entirely and add `VIRTUAL_HOST={{cookiecutter.domain_name}}` to your env file.
This pass all incoming requests on `nginx-proxy` to the nginx service your application is using.

.. _nginx-proxy: https://github.com/jwilder/nginx-proxy

Postgres is saving its database files to `/data/{{cookiecutter.repo_name}}/postgres` by default. Change that if you wan't
something else and make sure to make backups since this is not done automatically.

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

   docker-compose run django python manage.py shell_plus

To get an output of all running containers.

To check your logs, run::

   docker-compose logs

If you want to scale your application, run::

   docker-compose scale django=4
   docker-compose scale celeryworker=2


**Don't run the scale command on postgres or celerybeat**

Once you are ready with your initial setup, you wan't to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run `docker-compose up` in your projects root directory.

If you are using `supervisor`, you can use this file as a starting point::

    [program:{{cookiecutter.repo_name}}]
    command=docker-compose up
    directory=/path/to/{{cookiecutter.repo_name}}
    redirect_stderr=true
    autostart=true
    autorestart=true
    priority=10


Place it in `/etc/supervisor/conf.d/{{cookiecutter.repo_name}}.conf` and run::

    supervisorctl reread
    supervisorctl start {{cookiecutter.repo_name}}

To get the status, run::

    supervisorctl status

If you have errors, you can always check your stack with `docker-compose`. Switch to your projects root directory and run::

    docker-compose ps
