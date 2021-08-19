Getting Up and Running Locally With Docker
==========================================

.. index:: Docker

The steps below will get you up and running with a local development environment.
All of these commands assume you are in the root of your generated project.

.. note::

    If you're new to Docker, please be aware that some resources are cached system-wide
    and might reappear if you generate a project multiple times with the same name (e.g.
    :ref:`this issue with Postgres <docker-postgres-auth-failed>`).


Prerequisites
-------------

* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.
* Pre-commit; refer to the official documentation for the `installation guide`_.

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/
.. _`pre-commit`: https://pre-commit.com/#install

Build the Stack
---------------

This can take a while, especially the first time you run this particular command on your development system::

    $ docker-compose -f local.yml build

Generally, if you want to emulate production environment use ``production.yml`` instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!

Before doing any git commit, `pre-commit`_ should be installed globally on your local machine, and then::

    $ git init
    $ pre-commit install

Failing to do so will result with a bunch of CI and Linter errors that can be avoided with pre-commit.


Run the Stack
-------------

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker-compose -f local.yml up

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``local.yml`` like this::

    $ export COMPOSE_FILE=local.yml

And then run::

    $ docker-compose up

To run in a detached (background) mode, just::

    $ docker-compose up -d


Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker-compose -f local.yml run --rm`` command: ::

    $ docker-compose -f local.yml run --rm django python manage.py migrate
    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

Here, ``django`` is the target service we are executing the commands against.


(Optionally) Designate your Docker Development Server IP
--------------------------------------------------------

When ``DEBUG`` is set to ``True``, the host is validated against ``['localhost', '127.0.0.1', '[::1]']``. This is adequate when running a ``virtualenv``. For Docker, in the ``config.settings.local``, add your host development server IP to ``INTERNAL_IPS`` or ``ALLOWED_HOSTS`` if the variable exists.


.. _envs:

Configuring the Environment
---------------------------

This is the excerpt from your project's ``local.yml``: ::

  # ...

  postgres:
    build:
      context: .
      dockerfile: ./compose/production/postgres/Dockerfile
    volumes:
      - local_postgres_data:/var/lib/postgresql/data
      - local_postgres_data_backups:/backups
    env_file:
      - ./.envs/.local/.postgres

  # ...

The most important thing for us here now is ``env_file`` section enlisting ``./.envs/.local/.postgres``. Generally, the stack's behavior is governed by a number of environment variables (`env(s)`, for short) residing in ``envs/``, for instance, this is what we generate for you: ::

    .envs
    ├── .local
    │   ├── .django
    │   └── .postgres
    └── .production
        ├── .django
        └── .postgres

By convention, for any service ``sI`` in environment ``e`` (you know ``someenv`` is an environment when there is a ``someenv.yml`` file in the project root), given ``sI`` requires configuration, a ``.envs/.e/.sI`` `service configuration` file exists.

Consider the aforementioned ``.envs/.local/.postgres``: ::

    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_DB=<your project slug>
    POSTGRES_USER=XgOWtQtJecsAbaIyslwGvFvPawftNaqO
    POSTGRES_PASSWORD=jSljDz4whHuwO3aJIgVBrqEml5Ycbghorep4uVJ4xjDYQu0LfuTZdctj7y0YcCLu

The three envs we are presented with here are ``POSTGRES_DB``, ``POSTGRES_USER``, and ``POSTGRES_PASSWORD`` (by the way, their values have also been generated for you). You might have figured out already where these definitions will end up; it's all the same with ``django`` service container envs.

One final touch: should you ever need to merge ``.envs/.production/*`` in a single ``.env`` run the ``merge_production_dotenvs_in_dotenv.py``: ::

    $ python merge_production_dotenvs_in_dotenv.py

The ``.env`` file will then be created, with all your production envs residing beside each other.


Tips & Tricks
-------------

Activate a Docker Machine
~~~~~~~~~~~~~~~~~~~~~~~~~

This tells our computer that all future commands are specifically for the dev1 machine. Using the ``eval`` command we can switch machines as needed.::

    $ eval "$(docker-machine env dev1)"

Debugging
~~~~~~~~~

ipdb
"""""

If you are using the following within your code to debug: ::

    import ipdb; ipdb.set_trace()

Then you may need to run the following for it to work as desired: ::

    $ docker-compose -f local.yml run --rm --service-ports django


django-debug-toolbar
""""""""""""""""""""

In order for ``django-debug-toolbar`` to work designate your Docker Machine IP with ``INTERNAL_IPS`` in ``local.py``.


docker
""""""

The ``container_name`` from the yml file can be used to check on containers with docker commands, for example: ::

    $ docker logs worker
    $ docker top worker


Mailhog
~~~~~~~

When developing locally you can go with MailHog_ for email testing provided ``use_mailhog`` was set to ``y`` on setup. To proceed,

#. make sure ``mailhog`` container is up and running;

#. open up ``http://127.0.0.1:8025``.

.. _Mailhog: https://github.com/mailhog/MailHog/

.. _`CeleryTasks`:

Celery tasks in local development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When not using docker Celery tasks are set to run in Eager mode, so that a full stack is not needed. When using docker the task scheduler will be used by default.

If you need tasks to be executed on the main thread during development set CELERY_TASK_ALWAYS_EAGER = True in config/settings/local.py.

Possible uses could be for testing, or ease of profiling with DJDT.

.. _`CeleryFlower`:

Celery Flower
~~~~~~~~~~~~~

`Flower`_ is a "real-time monitor and web admin for Celery distributed task queue".

Prerequisites:

* ``use_docker`` was set to ``y`` on project initialization;
* ``use_celery`` was set to ``y`` on project initialization.

By default, it's enabled both in local and production environments (``local.yml`` and ``production.yml`` Docker Compose configs, respectively) through a ``flower`` service. For added security, ``flower`` requires its clients to provide authentication credentials specified as the corresponding environments' ``.envs/.local/.django`` and ``.envs/.production/.django`` ``CELERY_FLOWER_USER`` and ``CELERY_FLOWER_PASSWORD`` environment variables. Check out ``localhost:5555`` and see for yourself.

.. _`Flower`: https://github.com/mher/flower

Developing locally with HTTPS
-----------------------------

Increasingly it is becoming necessary to develop software in a secure environment in order that there are very few changes when deploying to production. Recently Facebook changed their policies for apps/sites that use Facebook login which requires the use of an HTTPS URL for the OAuth redirect URL. So if you want to use the ``users`` application with a OAuth provider such as Facebook, securing your communication to the local development environment will be necessary.

In order to create a secure environment, we need to have a trusted SSL certficate installed in our Docker application.

#.  **Let's Encrypt**
    
    The official line from Let’s Encrypt is: 

    [For local development section] ... The best option: Generate your own certificate, either self-signed or signed by a local root, and trust it in your operating system’s trust store. Then use that certificate in your local web server. See below for details. 

    See `letsencrypt.org - certificates-for-localhost`_

    .. _`letsencrypt.org - certificates-for-localhost`: https://letsencrypt.org/docs/certificates-for-localhost/

#.  **mkcert: Valid Https Certificates For Localhost**
    
    `mkcert`_ is a simple by design tool that hides all the arcane knowledge required to generate valid TLS certificates. It works for any hostname or IP, including localhost. It supports macOS, Linux, and Windows, and Firefox, Chrome and Java. It even works on mobile devices with a couple manual steps.

    See https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/

    .. _`mkcert`:  https://github.com/FiloSottile/mkcert/blob/master/README.md#supported-root-stores

After installing a trusted TLS certificate, configure your docker installation. We are going to configure an ``nginx`` reverse-proxy server. This makes sure that it does not interfere with our ``traefik`` configuration that is reserved for production environments.

These are the places that you should configure to secure your local environment.

certs
~~~~~

Take the certificates that you generated and place them in a folder called ``certs`` in the project's root folder. Assuming that you registered your local hostname as ``my-dev-env.local``, the certificates you will put in the folder should have the names ``my-dev-env.local.crt`` and ``my-dev-env.local.key``.

local.yml
~~~~~~~~~

#. Add the ``nginx-proxy`` service. ::

    ...

    nginx-proxy:
      image: jwilder/nginx-proxy:alpine
      container_name: nginx-proxy
      ports:
        - "80:80"
        - "443:443"
      volumes:
        - /var/run/docker.sock:/tmp/docker.sock:ro
        - ./certs:/etc/nginx/certs
      restart: always
      depends_on:
        - django
    
    ...

#. Link the ``nginx-proxy`` to ``django`` through environment variables.
   
   ``django`` already has an ``.env`` file connected to it. Add the following variables. You should do this especially if you are working with a team and you want to keep your local environment details to yourself.

   ::

      # HTTPS
      # ------------------------------------------------------------------------------
      VIRTUAL_HOST=my-dev-env.local
      VIRTUAL_PORT=8000

   The services run behind the reverse proxy.

config/settings/local.py
~~~~~~~~~~~~~~~~~~~~~~~~

You should allow the new hostname. ::

  ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "my-dev-env.local"]

Rebuild your ``docker`` application. ::

  $ docker-compose -f local.yml up -d --build

Go to your browser and type in your URL bar ``https://my-dev-env.local``

See `https with nginx`_ for more information on this configuration.

  .. _`https with nginx`: https://codewithhugo.com/docker-compose-local-https/

.gitignore
~~~~~~~~~~

Add ``certs/*`` to the ``.gitignore`` file. This allows the folder to be included in the repo but its contents to be ignored.

*This configuration is for local development environments only. Do not use this for production since you might expose your local* ``rootCA-key.pem``.
