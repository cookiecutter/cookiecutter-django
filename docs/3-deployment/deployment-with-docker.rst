Deployment with Docker
======================

.. index:: deployment, docker, docker compose, compose


Prerequisites
-------------

* Docker 17.05+.
* Docker Compose 1.17+


Understanding the Docker Compose Setup
--------------------------------------

Before you begin, check out the ``docker-compose.production.yml`` file in the root of this project. Keep note of how it provides configuration for the following services:

* ``django``: your application running behind ``Gunicorn``;
* ``postgres``: PostgreSQL database with the application's relational data;
* ``redis``: Redis instance for caching;
* ``traefik``: Traefik reverse proxy with HTTPS on by default.

Provided you have opted for Celery (via setting ``use_celery`` to ``y``) there are three more services:

* ``celeryworker`` running a Celery worker process;
* ``celerybeat`` running a Celery beat process;
* ``flower`` running Flower_.

The ``flower`` service is served by Traefik over HTTPS, through the port ``5555``. For more information about Flower and its login credentials, check out :ref:`CeleryFlower` instructions for local environment.

.. _`Flower`: https://github.com/mher/flower


Configuring the Stack
---------------------

The majority of services above are configured through the use of environment variables. Just check out :ref:`envs` and you will know the drill.

To obtain logs and information about crashes in a production setup, make sure that you have access to an external Sentry instance (e.g. by creating an account with `sentry.io`_), and set the ``SENTRY_DSN`` variable. Logs of level `logging.ERROR` are sent as Sentry events. Therefore, in order to send a Sentry event use:

.. code-block:: python

    import logging
    logging.error("This event is sent to Sentry", extra={"<example_key>": "<example_value>"})

The `extra` parameter allows you to send additional information about the context of this error.


You will probably also need to setup the Mail backend, for example by adding a `Mailgun`_ API key and a `Mailgun`_ sender domain, otherwise, the account creation view will crash and result in a 500 error when the backend attempts to send an email to the account owner.

.. _sentry.io: https://sentry.io/welcome
.. _Mailgun: https://mailgun.com


.. warning::

    .. include:: ../includes/mailgun.rst


Optional: Use AWS IAM Role for EC2 instance
-------------------------------------------

If you are deploying to AWS, you can use the IAM role to substitute AWS credentials, after which it's safe to remove the ``AWS_ACCESS_KEY_ID`` AND ``AWS_SECRET_ACCESS_KEY`` from ``.envs/.production/.django``. To do it, create an `IAM role`_ and `attach`_ it to the existing EC2 instance or create a new EC2 instance with that role. The role should assume, at minimum, the ``AmazonS3FullAccess`` permission.

.. _IAM role: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
.. _attach: https://aws.amazon.com/blogs/security/easily-replace-or-attach-an-iam-role-to-an-existing-ec2-instance-by-using-the-ec2-console/


HTTPS is On by Default
----------------------

SSL (Secure Sockets Layer) is a standard security technology for establishing an encrypted link between a server and a client, typically in this case, a web server (website) and a browser. Not having HTTPS means that malicious network users can sniff authentication credentials between your website and end users' browser.

It is always better to deploy a site behind HTTPS and will become crucial as the web services extend to the IoT (Internet of Things). For this reason, we have set up a number of security defaults to help make your website secure:

* If you are not using a subdomain of the domain name set in the project, then remember to put your staging/production IP address in the ``DJANGO_ALLOWED_HOSTS`` environment variable (see :ref:`settings`) before you deploy your website. Failure to do this will mean you will not have access to your website through the HTTP protocol.

* Access to the Django admin is set up by default to require HTTPS in production or once *live*.

The Traefik reverse proxy used in the default configuration will get you a valid certificate from Lets Encrypt and update it automatically. All you need to do to enable this is to make sure that your DNS records are pointing to the server Traefik runs on.

You can read more about this feature and how to configure it, at `Automatic HTTPS`_ in the Traefik docs.

.. _Automatic HTTPS: https://docs.traefik.io/https/acme/

.. _webpack-whitenoise-limitation:

Webpack without Whitenoise limitation
-------------------------------------

If you opt for Webpack without Whitenoise, Webpack needs to know the static URL at build time, when running ``docker compose build`` (See ``webpack/prod.config.js``). Depending on your setup, this URL may come from the following environment variables:

- ``AWS_STORAGE_BUCKET_NAME``
- ``DJANGO_AWS_S3_CUSTOM_DOMAIN``
- ``DJANGO_GCP_STORAGE_BUCKET_NAME``
- ``DJANGO_AZURE_CONTAINER_NAME``

The Django settings are getting these values at runtime via the ``.envs/.production/.django`` file , but Docker does not read this file at build time, it only look for a ``.env`` in the root of the project. Failing to pass the values correctly will result in a page without CSS styles nor javascript.

To solve this, you can either:

1. merge all the env files into ``.env`` by running::

     merge_production_dotenvs_in_dotenv.py

2. create a ``.env`` file in the root of the project with just variables you need. You'll need to also define them in ``.envs/.production/.django`` (hence duplicating them).
3. set these variables when running the build command::

     DJANGO_AWS_S3_CUSTOM_DOMAIN=example.com docker compose -f docker-compose.production.yml build``.

None of these options are ideal, we're open to suggestions on how to improve this. If you think you have one, please open an issue or a pull request.

(Optional) Postgres Data Volume Modifications
---------------------------------------------

Postgres is saving its database files to the ``production_postgres_data`` volume by default. Change that if you want something else and make sure to make backups since this is not done automatically.


Building & Running Production Stack
-----------------------------------

You will need to build the stack first. To do that, run::

    docker compose -f docker-compose.production.yml build

Once this is ready, you can run it with::

    docker compose -f docker-compose.production.yml up

To run the stack and detach the containers, run::

    docker compose -f docker-compose.production.yml up -d

To run a migration, open up a second terminal and run::

   docker compose -f docker-compose.production.yml run --rm django python manage.py migrate

To create a superuser, run::

   docker compose -f docker-compose.production.yml run --rm django python manage.py createsuperuser

If you need a shell, run::

   docker compose -f docker-compose.production.yml run --rm django python manage.py shell

To check the logs out, run::

   docker compose -f docker-compose.production.yml logs

If you want to scale your application, run::

   docker compose -f docker-compose.production.yml up --scale django=4
   docker compose -f docker-compose.production.yml up --scale celeryworker=2

.. warning:: don't try to scale ``postgres``, ``celerybeat``, or ``traefik``.

To see how your containers are doing run::

    docker compose -f docker-compose.production.yml ps


Example: Supervisor
-------------------

Once you are ready with your initial setup, you want to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run ``docker compose -f docker-compose.production.yml up`` in your projects root directory.

If you are using ``supervisor``, you can use this file as a starting point::

    [program:{{cookiecutter.project_slug}}]
    command=docker compose -f docker-compose.production.yml up
    directory=/path/to/{{cookiecutter.project_slug}}
    redirect_stderr=true
    autostart=true
    autorestart=true
    priority=10

Move it to ``/etc/supervisor/conf.d/{{cookiecutter.project_slug}}.conf`` and run::

    supervisorctl reread
    supervisorctl update
    supervisorctl start {{cookiecutter.project_slug}}

For status check, run::

    supervisorctl status

Media files without cloud provider
----------------------------------

If you chose no cloud provider and Docker, the media files will be served by an nginx service, from a ``production_django_media`` volume. Make sure to keep this around to avoid losing any media files.
