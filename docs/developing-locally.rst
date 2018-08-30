Getting Up and Running Locally
==============================

.. index:: pip, virtualenv, PostgreSQL


Setting Up Development Environment
----------------------------------

Make sure to have the following on your host:

* virtualenv_;
* pip;
* PostgreSQL.

First things first.

#. `Create a virtualenv`_.

#. Activate the virtualenv you have just created.

#. Install development requirements: ::

    $ pip install -r requirements/local.txt

#. Create a new PostgreSQL database (note: if this is the first time a database is created on your machine you might need to alter a localhost-related entry in your ``pg_hba.conf`` so as to utilize ``trust`` policy): ::

    $ createdb <what you've entered as the project_slug at setup stage>

#. Apply migrations: ::

    $ python manage.py migrate

#. See the application being served through Django development server: ::

    $ python manage.py runserver 0.0.0.0:8000

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _`Create a virtualenv`: https://virtualenv.pypa.io/en/stable/userguide/


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

.. _`Download the latest MailHog release`: https://github.com/mailhog/MailHog/releases
.. _`properly configured`: https://docs.djangoproject.com/en/dev/topics/email/#smtp-backend


Console
~~~~~~~

.. note:: If you have generated your project with ``use_mailhog`` set to ``n`` this will be a default setup.

Alternatively, deliver emails over console via ``EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'``.

In production, we have Mailgun_ configured to have your back!

.. _Mailgun: https://www.mailgun.com/


Sass Compilation & Live Reloading
---------------------------------

If you’d like to take advantage of live reloading and Sass / Compass CSS compilation you can do so with a little bit of preparation_.


.. _preparation: https://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html


Summary
-------

Congratulations, you have made it! Keep on reading to unleash full potential of Cookiecutter Django.
