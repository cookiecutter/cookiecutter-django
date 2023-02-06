Getting Up and Running Locally
==============================

.. index:: pip, virtualenv, PostgreSQL


Setting Up Development Environment
----------------------------------

Make sure to have the following on your host:

* Python 3.10
* PostgreSQL_.
* Redis_, if using Celery
* Cookiecutter_

First things first.

#. Create a virtualenv: ::

    $ python3.10 -m venv <virtual env path>

#. Activate the virtualenv you have just created: ::

    $ source <virtual env path>/bin/activate

#.
    .. include:: generate-project-block.rst

#. Install development requirements: ::

    $ cd <what you have entered as the project_slug at setup stage>
    $ pip install -r requirements/local.txt
    $ git init # A git repo is required for pre-commit to install
    $ pre-commit install

   .. note::

       the `pre-commit` hook exists in the generated project as default.
       For the details of `pre-commit`, follow the `pre-commit`_ site.

#. Create a new PostgreSQL database using createdb_: ::

    $ createdb --username=postgres <project_slug>

   ``project_slug`` is what you have entered as the project_slug at the setup stage.

   .. note::

       if this is the first time a database is created on your machine you might need an
       `initial PostgreSQL set up`_ to allow local connections & set a password for
       the ``postgres`` user. The `postgres documentation`_ explains the syntax of the config file
       that you need to change.


#. Set the environment variables for your database(s): ::

    $ export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/<DB name given to createdb>
    # Optional: set broker URL if using Celery
    $ export CELERY_BROKER_URL=redis://localhost:6379/0

   .. note::

       Check out the :ref:`settings` page for a comprehensive list of the environments variables.

   .. seealso::

       To help setting up your environment variables, you have a few options:

       * create an ``.env`` file in the root of your project and define all the variables you need in it.
         Then you just need to have ``DJANGO_READ_DOT_ENV_FILE=True`` in your machine and all the variables
         will be read.
       * Use a local environment manager like `direnv`_

#. Apply migrations: ::

    $ python manage.py migrate

#. If you're running synchronously, see the application being served through Django development server: ::

    $ python manage.py runserver 0.0.0.0:8000

or if you're running asynchronously: ::

    $ uvicorn config.asgi:application --host 0.0.0.0 --reload --reload-include '*.html'

.. _PostgreSQL: https://www.postgresql.org/download/
.. _Redis: https://redis.io/download
.. _CookieCutter: https://github.com/cookiecutter/cookiecutter
.. _createdb: https://www.postgresql.org/docs/current/static/app-createdb.html
.. _initial PostgreSQL set up: https://web.archive.org/web/20190303010033/http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html
.. _postgres documentation: https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html
.. _pre-commit: https://pre-commit.com/
.. _direnv: https://direnv.net/


Setup Email Backend
-------------------

MailHog
~~~~~~~

.. note:: In order for the project to support MailHog_ it must have been bootstrapped with ``use_mailhog`` set to ``y``.

MailHog is used to receive emails during development, it is written in Go and has no external dependencies.

For instance, one of the packages we depend upon, ``django-allauth`` sends verification emails to new users signing up as well as to the existing ones who have not yet verified themselves.

#. `Download the latest MailHog release`_ for your OS.

#. Rename the build to ``MailHog``.

#. Copy the file to the project root.

#. Make it executable: ::

    $ chmod +x MailHog

#. Spin up another terminal window and start it there: ::

    ./MailHog

#. Check out `<http://127.0.0.1:8025/>`_ to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

.. _`Download the latest MailHog release`: https://github.com/mailhog/MailHog

Console
~~~~~~~

.. note:: If you have generated your project with ``use_mailhog`` set to ``n`` this will be a default setup.

Alternatively, deliver emails over console via ``EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'``.

In production, we have Mailgun_ configured to have your back!

.. _Mailgun: https://www.mailgun.com/


Celery
------

If the project is configured to use Celery as a task scheduler then, by default, tasks are set to run on the main thread when developing locally instead of getting sent to a broker. However, if you have Redis setup on your local machine, you can set the following in ``config/settings/local.py``::

    CELERY_TASK_ALWAYS_EAGER = False

Next, make sure `redis-server` is installed (per the `Getting started with Redis`_ guide) and run the server in one terminal::

    $ redis-server

Start the Celery worker by running the following command in another terminal::

    $ celery -A config.celery_app worker --loglevel=info

That Celery worker should be running whenever your app is running, typically as a background process,
so that it can pick up any tasks that get queued. Learn more from the `Celery Workers Guide`_.

The project comes with a simple task for manual testing purposes, inside `<project_slug>/users/tasks.py`. To queue that task locally, start the Django shell, import the task, and call `delay()` on it::

    $ python manage.py shell
    >> from <project_slug>.users.tasks import get_users_count
    >> get_users_count.delay()

You can also use Django admin to queue up tasks, thanks to the `django-celerybeat`_ package.

.. _Getting started with Redis guide: https://redis.io/docs/getting-started/
.. _Celery Workers Guide: https://docs.celeryq.dev/en/stable/userguide/workers.html
.. _django-celerybeat: https://django-celery-beat.readthedocs.io/en/latest/


Sass Compilation & Live Reloading
---------------------------------

If you've opted for Gulp or Webpack as front-end pipeline, the project comes configured with `Sass`_ compilation and `live reloading`_. As you change you Sass/JS source files, the task runner will automatically rebuild the corresponding CSS and JS assets and reload them in your browser without refreshing the page.

#. Make sure that `Node.js`_ v16 is installed on your machine.
#. In the project root, install the JS dependencies with::

    $ npm install

#. Now - with your virtualenv activated - start the application by running::

    $ npm run dev

   The app will now run with live reloading enabled, applying front-end changes dynamically.

.. note:: The task will start 2 processes in parallel: the static assets build loop on one side, and the Django server on the other. You do NOT need to run Django as your would normally with ``manage.py runserver``.

.. _Node.js: http://nodejs.org/download/
.. _Sass: https://sass-lang.com/
.. _live reloading: https://browsersync.io

Summary
-------

Congratulations, you have made it! Keep on reading to unleash full potential of Cookiecutter Django.
