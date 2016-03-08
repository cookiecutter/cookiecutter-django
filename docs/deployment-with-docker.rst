Deployment with Docker
=================================================

.. index:: Docker, deployment

TODO: Review and revise

**Warning**

Docker is evolving extremely fast, but it has still some rough edges here and there. Compose is currently (as of version 1.4)
not considered production ready. That means you won't be able to scale to multiple servers and you won't be able to run
zero downtime deployments out of the box. Consider all this as experimental until you understand all the  implications
to run docker (with compose) on production.

**Run your app with docker-compose**

Prerequisites:

* docker (at least 1.10)
* docker-compose (at least 1.6)

Before you start, check out the `docker-compose.yml` file in the root of this project. This is where each component
of this application gets its configuration from. It consists of a `postgres` service that runs the database, `redis`
for caching, `nginx` as reverse proxy and last but not least the `django` application run by gunicorn.
{% if cookiecutter.use_celery == 'y' -%}
Since this application also runs Celery, there are two more services with a service called `celeryworker` that runs the
celery worker process and `celerybeat` that runs the celery beat process.
{% endif %}


All of these services except `redis` rely on environment variables set by you. There is an `env.example` file in the
root directory of this project as a starting point. Add your own variables to the file and rename it to `.env`. This
file won't be tracked by git by default so you'll have to make sure to use some other mechanism to copy your secret if
you are relying solely on git.


By default, the application is configured to listen on all interfaces on port 80. If you want to change that, open the
`docker-compose.yml` file and replace `0.0.0.0` with your own ip. If you are using `nginx-proxy`_ to run multiple
application stacks on one host, remove the port setting entirely and add `VIRTUAL_HOST={{cookiecutter.domain_name}}` to your env file.
This pass all incoming requests on `nginx-proxy`_ to the nginx service your application is using.

.. _nginx-proxy: https://github.com/jwilder/nginx-proxy

Postgres is saving its database files to `/data/{{cookiecutter.repo_name}}/postgres` by default. Change that if you wan't
something else and make sure to make backups since this is not done automatically.

To get started, pull your code from source control (don't forget the `.env` file) and change to your projects root
directory.

You'll need to build the stack first. To do that, run::

    docker-compose build

Once this is ready, you can run it with::

    docker-compose up


To run a migration, open up a second terminal and run::

   docker-compose run django python manage.py migrate

To create a superuser, run::

   docker-compose run django python manage.py createsuperuser


If you need a shell, run::

   docker-compose run django python manage.py shell

To get an output of all running containers.

To check your logs, run::

   docker-compose logs

If you want to scale your application, run::

   docker-compose scale django=4
   docker-compose scale celeryworker=2


**Don't run the scale command on postgres or celerybeat**

Once you are ready with your initial setup, you wan't to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run `docker-compose up` in your projects root directory.

If you are using `supervisor`, you can use this file as a starting point::

    [program:{{cookiecutter.repo_name}}]
    command=docker-compose up
    directory=/path/to/{{cookiecutter.repo_name}}
    redirect_stderr=true
    autostart=true
    autorestart=true
    priority=10


Place it in `/etc/supervisor/conf.d/{{cookiecutter.repo_name}}.conf` and run::

    supervisorctl reread
    supervisorctl start {{cookiecutter.repo_name}}

To get the status, run::

    supervisorctl status

If you have errors, you can always check your stack with `docker-compose`. Switch to your projects root directory and run::

    docker-compose ps
