Deployment on PythonAnywhere
============================

.. index:: PythonAnywhere


Overview
--------

Full instructions follow, but here's a high-level view.

**First time config**:

1. Pull your code down to PythonAnywhere using a *Bash console* and setup a virtualenv

2. Set your config variables in the *postactivate* script

3. Run the *manage.py* ``migrate`` and ``collectstatic`` commands. If you've opted for django-compressor, also run ``compress``

4. Add an entry to the PythonAnywhere *Web tab*

5. Set your config variables in the PythonAnywhere *WSGI config file*


Once you've been through this one-off config, future deployments are much simpler: just ``git pull`` and then hit the "Reload" button :)


Getting your code and dependencies installed on PythonAnywhere
--------------------------------------------------------------

Make sure your project is fully committed and pushed up to Bitbucket or Github or wherever it may be.  Then, log into your PythonAnywhere account, open up a **Bash** console, clone your repo, and create a virtualenv:

.. code-block:: bash

    git clone <my-repo-url>  # you can also use hg
    cd my-project-name
    mkvirtualenv --python=/usr/bin/python3.10 my-project-name
    pip install -r requirements/production.txt  # may take a few minutes

.. note:: We're creating the virtualenv using Python 3.10 (``--python=/usr/bin/python3.10```), although Cookiecutter Django generates a project for Python 3.12. This is because, at time of writing, PythonAnywhere only supports Python 3.10. It shouldn't be a problem, but if is, you may try changing the Python version to 3.12 and see if it works. If it does, please let us know, or even better, submit a pull request to update this section.

Setting environment variables in the console
--------------------------------------------

Generate a secret key for yourself, eg like this:

.. code-block:: bash

    python -c 'import random;import string; print("".join(random.SystemRandom().choice(string.digits + string.ascii_letters + string.punctuation) for _ in range(50)))'

Make a note of it, since we'll need it here in the console and later on in the web app config tab.

Set environment variables via the virtualenv "postactivate" script (this will set them every time you use the virtualenv in a console):

.. code-block:: bash

    vi $VIRTUAL_ENV/bin/postactivate

.. note:: If you don't like vi, you can also edit this file via the PythonAnywhere "Files" menu; look in the ".virtualenvs" folder.

Add these exports

.. code-block:: bash

    export WEB_CONCURRENCY=4
    export DJANGO_SETTINGS_MODULE='config.settings.production'
    export DJANGO_SECRET_KEY='<secret key goes here>'
    export DJANGO_ALLOWED_HOSTS='<www.your-domain.com>'
    export DJANGO_ADMIN_URL='<not admin/>'
    export MAILGUN_API_KEY='<mailgun key>'
    export MAILGUN_DOMAIN='<mailgun sender domain (e.g. mg.yourdomain.com)>'
    export DJANGO_AWS_ACCESS_KEY_ID=
    export DJANGO_AWS_SECRET_ACCESS_KEY=
    export DJANGO_AWS_STORAGE_BUCKET_NAME=
    export DATABASE_URL='<see Database setup section below>'
    export REDIS_URL='<see Redis section below>'

.. note:: The AWS details are not required if you're using whitenoise or the built-in pythonanywhere static files service, but you do need to set them to blank, as above.


Database setup
--------------

Go to the PythonAnywhere **Databases tab** and configure your database.

* For Postgres, setup your superuser password, then open a Postgres console and run a ``CREATE DATABASE my-db-name``.  You should probably also set up a specific role and permissions for your app, rather than using the superuser credentials.  Make a note of the address and port of your postgres server.

* For MySQL, set the password and create a database. More info here: https://help.pythonanywhere.com/pages/UsingMySQL

* You can also use sqlite if you like!  Not recommended for anything beyond toy projects though.


Now go back to the *postactivate* script and set the ``DATABASE_URL`` environment variable:

.. code-block:: bash

    export DATABASE_URL='postgres://<postgres-username>:<postgres-password>@<postgres-address>:<postgres-port>/<database-name>'
    # or
    export DATABASE_URL='mysql://<pythonanywhere-username>:<mysql-password>@<mysql-address>/<database-name>'
    # or
    export DATABASE_URL='sqlite:////home/yourusername/path/to/db.sqlite'

If you're using MySQL, you may need to run ``pip install mysqlclient``, and maybe add ``mysqlclient`` to *requirements/production.txt* too.

Now run the migration, and collectstatic:

.. code-block:: bash

    source $VIRTUAL_ENV/bin/postactivate
    python manage.py migrate
    python manage.py collectstatic
    # if using django-compressor:
    python manage.py compress
    # and, optionally
    python manage.py createsuperuser


Redis
-----

PythonAnywhere does NOT `offer a built-in solution <https://www.pythonanywhere.com/forums/topic/1666/>`_ for Redis, however the production setup from Cookiecutter Django uses Redis as cache and requires one.

We recommend to signup to a separate service offering hosted Redis (e.g. `Redislab <https://redis.com/>`_) and use the URL they provide.


Configure the PythonAnywhere Web Tab
------------------------------------

Go to the PythonAnywhere **Web tab**, hit **Add new web app**, and choose **Manual Config**, and then the version of Python you used for your virtualenv.

.. note:: If you're using a custom domain (not on \*.pythonanywhere.com), then you'll need to set up a CNAME with your domain registrar.

When you're redirected back to the web app config screen, set the **path to your virtualenv**.  If you used virtualenvwrapper as above, you can just enter its name.

Click through to the **WSGI configuration file** link (near the top) and edit the wsgi file. Make it look something like this, repeating the environment variables you used earlier:


.. code-block:: python

    import os
    import sys
    path = '/home/<your-username>/<your-project-directory>'
    if path not in sys.path:
        sys.path.append(path)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
    os.environ['DJANGO_SECRET_KEY'] = '<as above>'
    os.environ['DJANGO_ALLOWED_HOSTS'] = '<as above>'
    os.environ['DJANGO_ADMIN_URL'] = '<as above>'
    os.environ['MAILGUN_API_KEY'] = '<as above>'
    os.environ['MAILGUN_DOMAIN'] = '<as above>'
    os.environ['DJANGO_AWS_ACCESS_KEY_ID'] = ''
    os.environ['DJANGO_AWS_SECRET_ACCESS_KEY'] = ''
    os.environ['DJANGO_AWS_STORAGE_BUCKET_NAME'] = ''
    os.environ['DATABASE_URL'] = '<as above>'

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()


Back on the Web tab, hit **Reload**, and your app should be live!


.. note:: You may see security warnings until you set up your SSL certificates. If you want to suppress them temporarily, set ``DJANGO_SECURE_SSL_REDIRECT`` to blank. Follow `these instructions <https://help.pythonanywhere.com/pages/HTTPSSetup>`_ to get SSL set up.



Optional: static files
----------------------

If you want to use the PythonAnywhere static files service instead of using whitenoise or S3, you'll find its configuration section on the Web tab.  Essentially you'll need an entry to match your ``STATIC_URL`` and ``STATIC_ROOT`` settings.  There's more info `in this article <https://help.pythonanywhere.com/pages/DjangoStaticFiles>`_.


Future deployments
------------------

For subsequent deployments, the procedure is much simpler.  In a Bash console:

.. code-block:: bash

    workon my-virtualenv-name
    cd project-directory
    git pull
    python manage.py migrate
    python manage.py collectstatic
    # if using django-compressor:
    python manage.py compress

And then go to the Web tab and hit **Reload**

.. note:: If you're really keen, you can set up git-push based deployments:  https://blog.pythonanywhere.com/87/
