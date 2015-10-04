Getting Up and Running with Docker
==================================

.. index:: Docker

The steps below will get you up and running with a local development environment.
All of these commands assume you are in the root of your generated project.

Prerequisites
--------------

If you don't already have these installed, get them all by installing `Docker Toolbox`_.

* docker
* docker-machine
* docker-compose
* virtualbox

.. _`Docker Toolbox`: https://github.com/docker/toolbox/releases

Create the Machine (Optional)
-------------------------------

On Ubuntu you have native Docker, so you don't need to create a VM with 
docker-machine to use it.

However, on Mac/Windows/other systems without native Docker, you'll want to 
start by creating a VM with docker-machine::

    $ docker-machine create --driver virtualbox dev1

**Note:** If you want to have more than one docker development environment, then
name them accordingly. Instead of 'dev1' you might have 'dev2', 'myproject',
'djangopackages', et al.

Get the IP Address
--------------------

Once your machine is up and running, run this::

    $ docker-machine ip dev1
    123.456.789.012

This is also the IP address where the Django project will be served from.

Saving changes
--------------

If you are using OS X or Windows, you need to create a /data partition inside the
virtual machine that runs the docker deamon in order make all changes persistent.
If you don't do that your /data directory will get wiped out on every reboot.

To create a persistent folder, log into the virtual machine by running::

    $ docker-machine ssh dev1
    $ sudo su
    $ echo 'ln -sfn /mnt/sda1/data /data' >> /var/lib/boot2docker/bootlocal.sh

In case you are wondering why you can't use a host volume to keep the files on
your mac: As of `boot2docker` 1.7 you'll run into permission problems with mounted
host volumes if the container creates his own user and chown's the directories
on the volume. Postgres is doing that, so we need this quick fix to ensure that
all development data persists.

Build the Stack
---------------

This can take a while, especially the first time you run this particular command
on your development system::

    $ docker-compose build

Boot the System
---------------

This brings up both Django and PostgreSQL. 

The first time it is run it might take a while to get started, but subsequent 
runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker-compose -f dev.yml up

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``dev.yml`` like this::

    $ export COMPOSE_FILE=dev.yml

And then run::

    $ docker-compose up
    
Running management commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with any shell command that we wish to run in our container, this is done 
using the ``docker-compose run`` command. 

To migrate your app and to create a superuser, run::

    $ docker-compose run django python manage.py migrate
    $ docker-compose run django python manage.py createsuperuser

Here we specify the ``django`` container as the location to run our management commands.

Production Mode
~~~~~~~~~~~~~~~~

Instead of using `dev.yml`, you would use `docker-compose.yml`.

Other Useful Tips
------------------

Make a machine the active unit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tells our computer that all future commands are specifically for the dev1 machine. 
Using the ``eval`` command we can switch machines as needed.

::

    $ eval "$(docker-machine env dev1)"

Detached Mode
~~~~~~~~~~~~~

If you want to run the stack in detached mode (in the background), use the ``-d`` argument:

::

    $ docker-compose up -d
