Getting Up and Running with Docker
==================================

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* docker
* docker-compose

Open a terminal at the project root and run the following for local development::

    $ docker-compose -f dev.yml up

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``dev.yml`` like this::

    $ export COMPOSE_FILE=dev.yml

And then run::

    $ docker-compose up


To migrate your app and to create a superuser, run::

    $ docker-compose run django python manage.py migrate

    $ docker-compose run django python manage.py createsuperuser


If you are using `boot2docker` to develop on OS X or Windows, you need to create a `/data` partition inside your boot2docker
vm to make all changes persistent. If you don't do that your `/data` directory will get wiped out on every reboot.

To create a persistent folder, log into the `boot2docker` vm by running::

    $ bootdocker ssh

And then::

    $ sudo su
    $ echo 'ln -sfn /mnt/sda1/data /data' >> /var/lib/boot2docker/bootlocal.sh

In case you are wondering why you can't use a host volume to keep the files on your mac: As of `boot2docker` 1.7 you'll
run into permission problems with mounted host volumes if the container creates his own user and `chown`s the directories
on the volume. Postgres is doing that, so we need this quick fix to ensure that all development data persists.
