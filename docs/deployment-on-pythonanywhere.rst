Deployment on Heroku
====================

.. index:: PythonAnywhere


Overview
--------

* Push your code up to a code-sharing site like Bitbucket or Github

* Pull your code down to PythonAnywhere using a *Bash console* and create a virtualenv

* Set your config environment variables in the *postactivate* script

* Run the *manage.py* ``migrate`` and ``collectstatic`` commands

* Add an entry to the PythonAnywhere *Web tab*

* Future deployments are just `git pull` and then hit the "Reload" button


Getting your code and dependencies installed on PythonAnywhere
--------------------------------------------------------------

Make sure your project is fully commited and pushed up to Bitbucket or Github or wherever it may be.  Then, log into your PythonAnywhere account, open up a **Bash** console, clone your repo, and create a virtualenv:

.. code-block:: bash

    git clone <my-repo-url>  # you can also use hg
    cd my-project-name
    mkvirtualenv --python=/usr/bin/python3.4 my-project-name # or python2.7, etc
    pip install -r requirements/production.txt  # may take a few minutes



Setting environment variables in the console
--------------------------------------------

Generate a secret key for yourself, eg like this:

.. code-block:: bash

    python -c 'import random; print("".join(random.SystemRandom().choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for _ in range(50)))'

Make a note of it, since we'll need it here in the console and later on in the web app config tab.

Set environment variables via the virtualenv "postactivate" script (this will set them every time you use the virtualenv in a console):

.. code-block:: bash

    vi $VIRTUAL_ENV/bin/postactivate

**TIP:** If you don't like vi, you can also edit this file via the PythonAnywhere "Files" menu; look in the *.virtualenvs* folder.

Add these exports

.. code-block:: bash

    export DJANGO_SETTINGS_MODULE='config.settings.production'
    export DJANGO_SECRET_KEY='<secret key goes here>'
    export SENDGRID_USERNAME='<sendgrid username>'
    export SENDGRID_PASSWORD='<sendgrid password>'
    export DJANGO_AWS_ACCESS_KEY_ID=
    export DJANGO_AWS_SECRET_ACCESS_KEY=
    export DJANGO_AWS_STORAGE_BUCKET_NAME=

TODO: replace sendgrid with mailgun

**NOTE:** The AWS details are not required if you're using whitenoise or the built-in pythonanywhere static files service, but you do need to set them to blank, as above


Database setup:
---------------

Go to the PythonAnywhere databases tab and configure your database.

* For Postgres, setup your superuser password, then open a Postgres console and run a `CREATE DATABASE my-db-name`.  You should probably also set up a specific role and permissions for your app, rather than using the superuser credentials.  Make a note of the address and port of your postgres server.

* For MySQL, set the password and create a database. More info here: https://help.pythonanywhere.com/pages/UsingMySQL 

* You can also use sqlite if you like!  Not recommended for anything beyond toy projects though.


Now go back to the *postactivate* script and set the ``DATABASE_URL`` environment variable:

.. code-block:: bash

    vi $VIRTUAL_ENV/bin/postactivate


.. code-block:: bash

    export DATABASE_URL='postgres://<postgres-username>:<postgres-password>@<postgres-address>:<postgres-port>/<database-name>'
    # or
    export DATABASE_URL='mysql://<pythonanywhere-username>:<mysql-password>@mysql.server/<database-name>'
    # or
    export DATABASE_URL='sqlite:////absolute/path/to/db.sqlite'

If you're using MySQL, you may need to run ``pip install MySQLdb``, and maybe add ``MySQLdb`` to *requirements/production.txt* too.

Now run the migration, and collectstatic:

.. code-block:: bash

    source $VIRTUAL_ENV/bin/postactivate
    python manage.py migrate
    python manage.py collectstatic
    # and, optionally
    python manage.py createsuperuser



Configure the PythonAnywhere Web Tab
------------------------------------

Go to the PythonAnywhere **Web** tab, hit **Add new web app**, and choose **Manual Config**, and then the version of Python you used for your virtualenv.

When you're redirected back to the web app config screen, set the path to your virtualenv.  If you used virtualenvwrapper as above, you can just enter its name.

Click through to the **WSGI configuration file** link (near the top) and edit the wsgi file. Make it look something like this, repeating the environment variables you used earlier:


.. code-block:: python

    import os
    import sys
    path = '/home/<your-username>/<your-project-directory>'
    if path not in sys.path:
        sys.path.append(path)

    os.environ['DATABASE_URL'] = '<database url as above>'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
    os.environ['DJANGO_SECRET_KEY'] = '<secret key as above>'
    os.environ['SENDGRID_PASSWORD'] = ''
    os.environ['SENDGRID_USERNAME'] = ''
    os.environ['DJANGO_AWS_ACCESS_KEY_ID'] = ''
    os.environ['DJANGO_AWS_SECRET_ACCESS_KEY'] = ''
    os.environ['DJANGO_AWS_STORAGE_BUCKET_NAME'] = ''

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

TODO: sendgrid -> mailgun

Back on the Web tab, hit **Reload**, and your app should be live!

NB - you will see security warnings until you set up your SSL certificates. If you
want to supress them temporarily, set ``DJANGO_SECURE_SSL_REDIRECT`` to blank.  Follow
the instructions here to get SSL set up: https://www.pythonanywhere.com/wiki/SSLOwnDomains 


Optional: static files
----------------------

If you want to use the PythonAnywhere static files service instead of using whitenoise or S3, you'll find its configuration section on the Web tab.  Essentially you'll need an entry to match your ``STATIC_URL`` and ``STATIC_ROOT`` settings.  There's more info here: https://www.pythonanywhere.com/wiki/DjangoStaticFiles 


Future deployments
------------------

For subsequent deployments, the procedure is much simpler.  In a Bash console:

.. code-block:: bash

    workon my-virtualenv-name
    cd project-directory
    git pull
    python manage.py migrate
    python manage.py collectstatic

And then go to the Web tab and hit **Reload**


