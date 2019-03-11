Getting Up and Running Locally
==============================

.. index:: pip, virtualenv, PostgreSQL


Setting Up Development Environment
----------------------------------

Make sure to have the following on your host:

* Python 3.6
* PostgreSQL_.
* Redis_, if using Celery

First things first.

#. Create a virtualenv: ::

    $ python3.6 -m venv <virtual env path>

#. Activate the virtualenv you have just created: ::

    $ source <virtual env path>/bin/activate

#. Install development requirements: ::

    $ pip install -r requirements/local.txt

#. Create a new PostgreSQL database using createdb_: ::

    $ createdb <what you have entered as the project_slug at setup stage> -U postgres --password <password>

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

#. See the application being served through Django development server: ::

    $ python manage.py runserver 0.0.0.0:8000

.. _PostgreSQL: https://www.postgresql.org/download/
.. _Redis: https://redis.io/download
.. _createdb: https://www.postgresql.org/docs/current/static/app-createdb.html
.. _initial PostgreSQL set up: http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html
.. _postgres documentation: https://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html
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
If the project is configured to use Celery as a task scheduler then by default tasks are set to run on the main thread
when developing locally. If you have the appropriate setup on your local machine then set

CELERY_TASK_ALWAYS_EAGER = False

in /config/settings/local.py


Sass Compilation & Live Reloading
---------------------------------

If you’d like to take advantage of live reloading and Sass compilation you can do so with a little
bit of preparation, see :ref:`sass-compilation-live-reload`.

Summary
-------

Congratulations, you have made it! Keep on reading to unleash full potential of Cookiecutter Django.
