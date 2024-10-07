Troubleshooting
===============

This page contains some advice about errors and problems commonly encountered during the development of Cookiecutter Django applications.

Server Error on sign-up/log-in
------------------------------

Make sure you have configured the mail backend (e.g. Mailgun) by adding the API key and sender domain

.. include:: ../includes/mailgun.rst

.. _docker-postgres-auth-failed:

Docker: Postgres authentication failed
--------------------------------------

Examples of logs::

    postgres_1      | 2018-06-07 19:11:23.963 UTC [81] FATAL:  password authentication failed for user "pydanny"
    postgres_1      | 2018-06-07 19:11:23.963 UTC [81] DETAIL:  Password does not match for user "pydanny".
    postgres_1      | 	Connection matched pg_hba.conf line 95: "host all all all md5"

If you recreate the project multiple times with the same name, Docker would preserve the volumes for the postgres container between projects. Here is what happens:

#. You generate the project the first time. The .env postgres file is populated with the random password
#. You run the docker compose and the containers are created. The postgres container creates the database based on the .env file credentials
#. You "regenerate" the project with the same name, so the postgres .env file is populated with a new random password
#. You run docker compose. Since the names of the containers are the same, docker will try to start them (not create them from scratch i.e. it won't execute the Dockerfile to recreate the database). When this happens, it tries to start the database based on the new credentials which do not match the ones that the database was created with, and you get the error message above.

To fix this, you can either:

- Clear your project-related Docker cache with ``docker compose -f docker-compose.local.yml down --volumes --rmi all``.
- Use the Docker volume sub-commands to find volumes (`ls`_) and remove them (`rm`_).
- Use the `prune`_ command to clear system-wide (use with care!).

.. _ls: https://docs.docker.com/engine/reference/commandline/volume_ls/
.. _rm: https://docs.docker.com/engine/reference/commandline/volume_rm/
.. _prune: https://docs.docker.com/v17.09/engine/reference/commandline/system_prune/

Variable is not set. Defaulting to a blank string
-------------------------------------------------

Example::

    WARN[0000] The "DJANGO_AWS_STORAGE_BUCKET_NAME" variable is not set. Defaulting to a blank string.
    WARN[0000] The "DJANGO_AWS_S3_CUSTOM_DOMAIN" variable is not set. Defaulting to a blank string.

You have probably opted for Docker + Webpack without Whitenoise. This is a know limitation of the combination, which needs a little bit of manual intervention. See the :ref:`dedicated section about it <webpack-whitenoise-limitation>`.

Others
------

#. ``project_slug`` must be a valid Python module name or you will have issues on imports.

#. ``jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'now'.``: please upgrade your cookiecutter version to >= 1.4 (see `#528`_)

#. New apps not getting created in project root: This is the expected behavior, because cookiecutter-django does not change the way that django startapp works, you'll have to fix this manually (see `#1725`_)

.. _#528: https://github.com/cookiecutter/cookiecutter-django/issues/528#issuecomment-212650373
.. _#1725: https://github.com/cookiecutter/cookiecutter-django/issues/1725#issuecomment-407493176
