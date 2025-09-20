Deployment on PythonAnywhere
============================

.. index:: PythonAnywhere


Overview
--------

Full instructions follow, but here's a high-level view.

**First time config**:

1. Pull your code down to PythonAnywhere using a *Bash console* and install your dependencies

2. Set your config variables in the *postactivate* script

3. Run the *manage.py* ``migrate`` and ``collectstatic`` commands. If you've opted for django-compressor, also run ``compress``

4. Add an entry to the PythonAnywhere *Web tab*

5. Set your config variables in the PythonAnywhere *WSGI config file*

Once you've been through this one-off config, future deployments are much simpler: just ``git pull`` and then hit the "Reload" button :)


Getting your code and dependencies installed on PythonAnywhere
--------------------------------------------------------------

Make sure your project is fully committed and pushed up to Github, GitLab or wherever it may be. Then, log into your PythonAnywhere account, open up a **Bash** console, clone your repo, and install your project:

.. code-block:: bash

    git clone <my-repo-url>
    cd my-project-name
    uv sync --locked --no-dev  # may take a few minutes


Setting environment variables
-----------------------------

Generate a secret key for yourself, e.g. like this:

.. code-block:: bash

    uv run python -c 'import secrets;import string; print("".join(secrets.choice(string.digits + string.ascii_letters + string.punctuation) for _ in range(50)))'

Make a note of it, since we'll need it here in the console and later on in the web app config tab.

Set environment variables via the ``.env`` file:

.. code-block:: bash

    vi .env

.. note:: If you don't like vi, you can also edit this file via the PythonAnywhere "Files" menu.

Add these env variables:

.. code-block:: bash

    WEB_CONCURRENCY=4
    DJANGO_SETTINGS_MODULE='config.settings.production'
    DJANGO_SECRET_KEY='<secret key goes here>'
    DJANGO_ALLOWED_HOSTS='<www.your-domain.com>'
    DJANGO_ADMIN_URL='<not admin/>'
    MAILGUN_API_KEY='<mailgun key>'
    MAILGUN_DOMAIN='<mailgun sender domain (e.g. mg.yourdomain.com)>'
    DJANGO_AWS_ACCESS_KEY_ID=
    DJANGO_AWS_SECRET_ACCESS_KEY=
    DJANGO_AWS_STORAGE_BUCKET_NAME=
    DATABASE_URL='<see Database setup section below>'
    REDIS_URL='<see Redis section below>'

.. note:: The AWS details are not required if you're using whitenoise or the built-in PythonAnywhere static files service, but you do need to set them to blank, as above.


Database setup
--------------

Go to the PythonAnywhere **Databases tab** and configure your database. Using Postgres, setup your superuser password, then open a Postgres console and run a ``CREATE DATABASE my-db-name``.  You should probably also set up a specific role and permissions for your app, rather than using the superuser credentials.  Make a note of the address and port of your postgres server.

Now go back to the ``.env`` file and set the ``DATABASE_URL`` environment variable:

.. code-block:: bash

    DATABASE_URL='postgres://<postgres-username>:<postgres-password>@<postgres-address>:<postgres-port>/<database-name>'

Now run the migration, and collectstatic:

.. code-block:: bash

    export UV_ENV_FILE=.env
    export UV_NO_DEV=1
    uv run python manage.py migrate
    uv run python manage.py compress  # optional, if using django-compressor
    uv run python manage.py collectstatic
    # and, optionally
    uv run python manage.py createsuperuser


Redis
-----

PythonAnywhere does NOT `offer a built-in solution <https://www.pythonanywhere.com/forums/topic/1666/>`_ for Redis, however the production setup from Cookiecutter Django uses Redis as cache and requires one.

We recommend to signup to a separate service offering hosted Redis (e.g. `Redislab <https://redis.com/>`_) and use the URL they provide.


Configure the PythonAnywhere Web Tab
------------------------------------

Go to the PythonAnywhere **Web tab**, hit **Add new web app**, and choose **Manual Config**, and then the Python 3.13.

.. note:: If you're using a custom domain (not on \*.pythonanywhere.com), then you'll need to set up a CNAME with your domain registrar.

When you're redirected back to the web app config screen, set the **path to your virtualenv**, which should be something like ``/home/<your-username>/<your-project-directory>/.venv``.

Click through to the **WSGI configuration file** link (near the top) and edit the wsgi file. Make it look something like this, repeating the environment variables you used earlier:

.. code-block:: python

    import os
    import sys
    PROJECT_PATH = '/home/<your-username>/<your-project-directory>'
    if PROJECT_PATH not in sys.path:
        sys.path.append(PROJECT_PATH)

    os.environ['DJANGO_SETTINGS_MODULE='] = 'config.settings.production'
    os.environ['DJANGO_READ_DOT_ENV_FILE'] = '1'

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

    cd project-directory
    git pull
    uv run python manage.py migrate
    uv run python manage.py compress  # optional, if using django-compressor
    uv run python manage.py collectstatic

And then go to the Web tab and hit **Reload**

.. note:: If you're really keen, you can set up git-push based deployments:  https://blog.pythonanywhere.com/87/
