Getting Up and Running Locally
==============================

.. index:: pip, virtualenv, PostgreSQL

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the os dependencies::

    $ sudo ./install_os_dependencies.sh install

Then install the requirements for your local development::

    $ pip install -r requirements/local.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then, create a PostgreSQL database with the following command, where `[project_slug]` is what value you entered for your project's `project_slug`::

    $ createdb [project_slug]

`cookiecutter-django` uses the excellent `django-environ`_ package with its ``DATABASE_URL`` environment variable to simplify database configuration in your Django settings. Now all you have to do is compose a definition for ``DATABASE_URL``:

.. parsed-literal::

    $ export DATABASE_URL="postgres://*<pg_user_name>*:*<pg_user_password>*\ @127.0.0.1:\ *<pg_port>*/*<pg_database_name>*"

.. _django-environ: http://django-environ.readthedocs.org

You can now run the usual Django ``migrate`` and ``runserver`` commands::

    $ python manage.py migrate
    $ python manage.py runserver

**Setup your email backend**

django-allauth sends an email to verify users (and superusers) after signup and login (if they are still not verified). To send email you need to `configure your email backend`_

.. _configure your email backend: http://docs.djangoproject.com/en/1.9/topics/email/#smtp-backend

In development you can (optionally) use MailHog_ for email testing. MailHog is built with Go so there are no dependencies. To use MailHog::

1. `Download the latest release`_ for your operating system
2. Rename the executable to ``mailhog`` and copy it to the root of your project directory
3. Make sure it is executable (e.g. ``chmod +x mailhog``)

.. _Mailhog: https://github.com/mailhog/MailHog/
.. _Download the latest release: https://github.com/mailhog/MailHog/releases

Alternatively simply output emails to the console via: ``EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'``

In production basic email configuration is setup to send emails with Mailgun_

.. _Mailgun: https://www.mailgun.com/

**Live reloading and Sass CSS compilation**

If you'd like to take advantage of live reloading and Sass / Compass CSS compilation you can do so with the included Grunt task.

Make sure that nodejs_ is installed. Then in the project root run::

    $ npm install

.. _nodejs: http://nodejs.org/download/

Now you just need::

    $ grunt serve

The base app will now run as it would with the usual ``manage.py runserver`` but with live reloading and Sass compilation enabled.

To get live reloading to work you'll probably need to install an `appropriate browser extension`_

.. _appropriate browser extension: http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-

It's time to write the code!!!
