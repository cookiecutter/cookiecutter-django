Getting Up and Running Locally With Docker
==========================================

.. index:: Docker

.. note::

    If you're new to Docker, please be aware that some resources are cached system-wide
    and might reappear if you generate a project multiple times with the same name (e.g.
    :ref:`this issue with Postgres <docker-postgres-auth-failed>`).


Prerequisites
-------------

* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.
* Pre-commit; refer to the official documentation for the `pre-commit`_.
* Cookiecutter; refer to the official GitHub repository of `Cookiecutter`_

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/
.. _`pre-commit`: https://pre-commit.com/#install
.. _`Cookiecutter`: https://github.com/cookiecutter/cookiecutter

Before Getting Started
----------------------
.. include:: generate-project-block.rst

Build the Stack
---------------

This can take a while, especially the first time you run this particular command on your development system::

    $ docker compose -f docker-compose.local.yml build

Generally, if you want to emulate production environment use ``docker-compose.production.yml`` instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!

Before doing any git commit, `pre-commit`_ should be installed globally on your local machine, and then::

    $ git init
    $ pre-commit install

Failing to do so will result with a bunch of CI and Linter errors that can be avoided with pre-commit.

Run the Stack
-------------

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker compose -f docker-compose.local.yml up

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``docker-compose.local.yml`` like this::

    $ export COMPOSE_FILE=docker-compose.local.yml

And then run::

    $ docker compose up

To run in a detached (background) mode, just::

    $ docker compose up -d

These commands don't run the docs service. In order to run docs service you can run::

    $ docker compose -f docker-compose.docs.yml up

To run the docs with local services just use::

    $ docker compose -f docker-compose.local.yml -f docker-compose.docs.yml up

The site should start and be accessible at http://localhost:3000 if you selected Webpack or Gulp as frontend pipeline and http://localhost:8000 otherwise.

Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker compose -f docker-compose.local.yml run --rm`` command: ::

    $ docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
    $ docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

Here, ``django`` is the target service we are executing the commands against.
Also, please note that the ``docker exec`` does not work for running management commands.

(Optionally) Designate your Docker Development Server IP
--------------------------------------------------------

When ``DEBUG`` is set to ``True``, the host is validated against ``['localhost', '127.0.0.1', '[::1]']``. This is adequate when running a ``virtualenv``. For Docker, in the ``config.settings.local``, add your host development server IP to ``INTERNAL_IPS`` or ``ALLOWED_HOSTS`` if the variable exists.

.. _envs:

Configuring the Environment
---------------------------

This is the excerpt from your project's ``docker-compose.local.yml``: ::

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
    │   ├── .django
    │   └── .postgres
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

Add 3rd party python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install a new 3rd party python package, you cannot use ``pip install <package_name>``, that would only add the package to the container. The container is ephemeral, so that new library won't be persisted if you run another container. Instead, you should modify the Docker image:
You have to modify the relevant requirement file: base, local or production by adding: ::

    <package_name>==<package_version>

To get this change picked up, you'll need to rebuild the image(s) and restart the running container: ::

    docker compose -f docker-compose.local.yml build
    docker compose -f docker-compose.local.yml up

Debugging
~~~~~~~~~

ipdb
"""""

If you are using the following within your code to debug: ::

    import ipdb; ipdb.set_trace()

Then you may need to run the following for it to work as desired: ::

    $ docker compose -f docker-compose.local.yml run --rm --service-ports django


django-debug-toolbar
""""""""""""""""""""

In order for ``django-debug-toolbar`` to work designate your Docker Machine IP with ``INTERNAL_IPS`` in ``local.py``.


docker
""""""

The ``container_name`` from the yml file can be used to check on containers with docker commands, for example: ::

    $ docker logs <project_slug>_local_celeryworker
    $ docker top <project_slug>_local_celeryworker

Notice that the ``container_name`` is generated dynamically using your project slug as a prefix

Mailpit
~~~~~~~

When developing locally you can go with Mailpit_ for email testing provided ``use_mailpit`` was set to ``y`` on setup. To proceed,

#. make sure ``<project_slug>_local_mailpit`` container is up and running;

#. open up ``http://127.0.0.1:8025``.

.. _Mailpit: https://github.com/axllent/mailpit/

.. _`CeleryTasks`:

Celery tasks in local development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When not using docker Celery tasks are set to run in Eager mode, so that a full stack is not needed. When using docker the task scheduler will be used by default.

If you need tasks to be executed on the main thread during development set ``CELERY_TASK_ALWAYS_EAGER = True`` in ``config/settings/local.py``.

Possible uses could be for testing, or ease of profiling with DJDT.

.. _`CeleryFlower`:

Celery Flower
~~~~~~~~~~~~~

`Flower`_ is a "real-time monitor and web admin for Celery distributed task queue".

Prerequisites:

* ``use_docker`` was set to ``y`` on project initialization;
* ``use_celery`` was set to ``y`` on project initialization.

By default, it's enabled both in local and production environments (``docker-compose.local.yml`` and ``docker-compose.production.yml`` Docker Compose configs, respectively) through a ``flower`` service. For added security, ``flower`` requires its clients to provide authentication credentials specified as the corresponding environments' ``.envs/.local/.django`` and ``.envs/.production/.django`` ``CELERY_FLOWER_USER`` and ``CELERY_FLOWER_PASSWORD`` environment variables. Check out ``localhost:5555`` and see for yourself.

.. _`Flower`: https://github.com/mher/flower

Using Webpack or Gulp
~~~~~~~~~~~~~~~~~~~~~

If you've opted for Gulp or Webpack as front-end pipeline, the project comes configured with `Sass`_ compilation and `live reloading`_. As you change your Sass/JS source files, the task runner will automatically rebuild the corresponding CSS and JS assets and reload them in your browser without refreshing the page.

The stack comes with a dedicated node service to build the static assets, watch for changes and proxy requests to the Django app with live reloading scripts injected in the response. For everything to work smoothly, you need to access the application at the port served by the node service, which is http://localhost:3000 by default.

.. _Sass: https://sass-lang.com/
.. _live reloading: https://browsersync.io


Using Just for Docker Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have included a ``justfile`` to simplify the use of frequent Docker commands for local development.

.. warning::
    Currently, "Just" does not reliably handle signals or forward them to its subprocesses. As a result,
    pressing CTRL+C (or sending other signals like SIGTERM, SIGINT, or SIGHUP) may only interrupt
    "Just" itself rather than its subprocesses.
    For more information, see `this GitHub issue <https://github.com/casey/just/issues/2473>`_.

First, install Just using one of the methods described in the `official documentation <https://just.systems/man/en/packages.html>`_.

Here are the available commands:

- ``just build``
  Builds the Python image using the local Docker Compose file.

- ``just up``
  Starts the containers in detached mode and removes orphaned containers.

- ``just down``
  Stops the running containers.

- ``just prune``
  Stops and removes containers along with their volumes. You can optionally pass an argument with the service name to prune a single container.

- ``just logs``
  Shows container logs. You can optionally pass an argument with the service name to view logs for a specific service.

- ``just manage <command>``
  Runs Django management commands within the container. Replace ``<command>`` with any valid Django management command, such as ``migrate``, ``createsuperuser``, or ``shell``.


(Optionally) Developing locally with HTTPS
------------------------------------------

Nginx
~~~~~

If you want to add some sort of social authentication with a OAuth provider such as Facebook, securing your communication to the local development environment will be necessary. These providers usually require that you use an HTTPS URL for the OAuth redirect URL for the Facebook login to work appropriately.

Here is a link to an article on `how to add HTTPS using Nginx`_ to your local docker installation. This also includes how to serve files from the ``media`` location, in the event that you are want to serve user-uploaded content.

.. _`how to add HTTPS using Nginx`: https://afroshok.com/cookiecutter-https

Webpack
~~~~~~~

If you are using Webpack, first install `mkcert`_. It is a simple by design tool that hides all the arcane knowledge required to generate valid TLS certificates. It works for any hostname or IP, including localhost. It supports macOS, Linux, and Windows, and Firefox, Chrome and Java. It even works on mobile devices with a couple manual steps. See https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/

.. _`mkcert`:  https://github.com/FiloSottile/mkcert/blob/master/README.md#supported-root-stores

These are the places that you should configure to secure your local environment. Take the certificates that you generated and place them in a folder called ``certs`` in the project's root folder. Configure an ``nginx`` reverse-proxy server as a ``service`` in the ``docker-compose.local.yml``. This makes sure that it does not interfere with our ``traefik`` configuration that is reserved for production environments.

Assuming that you registered your local hostname as ``my-dev-env.local``, the certificates you will put in the folder should have the names ``my-dev-env.local.crt`` and ``my-dev-env.local.key``.

1. Add the ``nginx-proxy`` service to the ``docker-compose.local.yml``. ::

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
        - node
      environment:
        - VIRTUAL_HOST=my-dev-env.local
        - VIRTUAL_PORT=3000

2. Add the local secure domain to the ``config/settings/local.py``. You should allow the new hostname ::

    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "my-dev-env.local"]

3. Add the following configuration to the ``devServer`` section of ``webpack/dev.config.js`` ::

    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws', // note the `:0` after `0.0.0.0`
    },


Rebuild your ``docker`` application. ::

    $ docker compose -f docker-compose.local.yml up -d --build

Go to your browser and type in your URL bar ``https://my-dev-env.local``.

For more on this configuration, see `https with nginx`_.

.. _`https with nginx`: https://codewithhugo.com/docker-compose-local-https/
