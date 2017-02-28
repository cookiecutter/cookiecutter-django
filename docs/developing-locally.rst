Getting Up and Running Locally
==============================

.. index:: pip, virtualenv, PostgreSQL

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_.

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then install the requirements for your local development::

    $ pip install -r requirements/local.txt

Then, create a PostgreSQL database with the following command, where `[project_slug]` is what value you entered for your project's `project_slug`::

    $ createdb [project_slug]

You can now run the usual Django ``migrate`` and ``runserver`` commands::

    $ python manage.py migrate
    $ python manage.py runserver

At this point you can take a break from setup and start getting to know the files in the project.

But if you want to go further with setup, read on.

(Note: the following sections still need to be revised)

Setting Up Env Vars for Production
-----------------------------------

`Cookiecutter Django` uses the excellent `django-environ`_ package, which includes a ``DATABASE_URL`` environment variable to simplify database configuration in your Django settings.

Rename env.example to .env to begin updating the file with your own environment variables. To add your database, define ``DATABASE_URL`` and add it to the .env file, as shown below:

.. parsed-literal::

    DATABASE_URL="postgres://*<pg_user_name>*:*<pg_user_password>*\ @127.0.0.1:\ *<pg_port>*/*<pg_database_name>*"

.. _django-environ: http://django-environ.readthedocs.io

Setup your email backend
-------------------------

django-allauth sends an email to verify users (and superusers) after signup and login (if they are still not verified). To send email you need to `configure your email backend`_

.. _configure your email backend: https://docs.djangoproject.com/en/dev/topics/email/#smtp-backend

In development you can (optionally) use MailHog_ for email testing. MailHog is built with Go so there are no dependencies. To use MailHog:

1. `Download the latest release`_ for your operating system
2. Rename the executable to ``mailhog`` and copy it to the root of your project directory
3. Make sure it is executable (e.g. ``chmod +x mailhog``)
4. Execute mailhog from the root of your project in a new terminal window (e.g. ``./mailhog``)
5. All emails generated from your django app can be seen on http://127.0.0.1:8025/

.. _Mailhog: https://github.com/mailhog/MailHog/
.. _Download the latest release: https://github.com/mailhog/MailHog/releases

Alternatively simply output emails to the console via: ``EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'``

In production basic email configuration is setup to send emails with Mailgun_

.. _Mailgun: https://www.mailgun.com/

**Live reloading and Sass CSS compilation**

If you’d like to take advantage of live reloading and Sass / Compass CSS compilation you can do so with a little bit of `prep work`_.

.. _prep work: https://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html
