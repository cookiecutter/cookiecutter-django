Getting Up and Running Locally
==============================

.. index:: pip, virtualenv, PostgreSQL

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then, create a PostgreSQL database and add the database configuration using the  ``dj-database-url`` app pattern: ``postgres://db_owner:password@dbserver_ip:port/db_name`` either:

* in the ``config.settings.common.py`` setting file,
* or in the environment variable ``DATABASE_URL``


You can now run the usual Django ``migrate`` and ``runserver`` command::

    $ python manage.py migrate

    $ python manage.py runserver

**Setup your email backend**

django-allauth sends an email to verify users (and superusers) after signup and login (if they are still not verified). To send email you need to `configure your email backend`_

.. _configure your email backend: http://docs.djangoproject.com/en/1.8/topics/email/#smtp-backend

In development you can (optionally) use Maildump_ for email testing. Or alternatively simply output emails to the console via: ``EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'``

.. _Maildump: https://github.com/ThiefMaster/maildump

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
