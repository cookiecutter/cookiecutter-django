# -*- coding: utf-8 -*-
"""
This is a collection of useful utility functions when working with docker on different environments.

In order to use these functions, install fabric on your local machine with::

    pip install fabric

Please note: Fabric is a remote code execution tool, NOT a remote configuration tool. While you can copy files
from here to there, it is not a good replacement for salt or ansible in this regard.

There is a function called `production` where you need to fill in the details about your production machine(s).

You can then run::

    fab production status

to get the status of your stack

To list all available commands, run::

    fab -l
"""

from __future__ import absolute_import, print_function, unicode_literals
from fabric.operations import local as lrun, run, sudo
from fabric.api import *
from fabric.colors import green, red, yellow
from fabric.contrib.console import confirm


def local():
    """
    Work on the local environment
    """
    env.compose_file = "dev.yml"
    env.project_dir = "."
    env.run = lrun
    env.cd = lcd


def production():
    """
    Work on the production environment
    """
    env.hosts = [""]  # list the ip addresses or domain names of your production boxes here
    env.port = 22  # ssh port
    env.user = "root"  # remote user, see `env.run` if you don't log in as root

    env.compose_file = "docker-compose.yml"
    env.project_dir = ""  # this is the project dir where your code lives on this machine

    # if you don't use key authentication, add your password here
    # env.password = "foobar"
    # if your machine has no bash installed, fall back to sh
    # env.shell = "/bin/sh -c"

    env.run = run  # if you don't log in as root, replace with 'env.run = sudo'
    env.cd = cd


def rollback(commit="HEAD~1"):
    """
    Rollback to a previous commit and build the stack
    :param commit: Commit you want to roll back to. Default is the previous commit
    """
    with env.cd(env.project_dir):
        env.run("git checkout {}".format(commit))

    docker_compose("build")


def deploy():
    """
    Pulls the latest changes from master, rebuilt and restarts the stack
    """
    with env.cd(env.project_dir):
        env.run("git pull origin master")

    build()
    restart()


def scale(service, n):
    """
    Scale a service
    :param service: Service to scale
    :param n: Number of containers
    """
    if service not in ["celeryworker"]:
        print(red("{} is not scalabale, aborting".format(service)))
        return
    docker_compose("scale {service} {n}".format(service=service, n=n))


def restart():
    """
    Restart all services
    """
    docker_compose("restart")


def build(cache=True):
    """
    Builds the the stack
    :param cache: Use docker cache. Default is True
    """
    docker_compose("build" if cache else "build --no-cache")


def status():
    """
    Display the status of all services
    """
    docker_compose("ps")


def django_shell():
    """
    Starts a Django shell
    """
    docker_compose("run django python manage.py shell")


def sql_shell():
    """
    Starts a postgres shell
    """
    _postgres("psql")


def migrate_database():
    """
    Run a Django database migration
    """
    docker_compose("run django python manage.py migrate")


def dump_database(filepath):
    """
    Dumps the database to a file
    :param filepath:
    """
    filepath = '/Users/j/test/dump.sql'

    # make sure that the directory exists
    with settings(warn_only=True):
        dir = "/".join(filepath.split("/")[:-1])
        if env.run("cd {}".format(dir)).return_code != 0:
            print(red("{dir} does not exist. Make sure to create the directory before creating a"
                      " database dump to it.".format(dir=dir)))
            print(red("Aborting"))
            return

    _postgres(command="pg_dump", pipe_out="> " + filepath)


def restore_database(filepath):
    """
    Restores the database from a sql file (Not yet implemented)
    :param filepath:
    """
    # that's a bit tricky because we can't pipe in from stdin. We need to mount a volume that contains the dump
    # and pipe it in from there. Compose doesn't support mounting volumes in `run` yet, so we'll have to wait.
    # see https://github.com/docker/compose/issues/1769
    print(red("Not yet implemented"))


def drop_database():
    """
    Drop the database (Not yet implemented)
    """
    print(red("Not yet implemented"))
    return
    print(red("****************************************************"))
    print(red("*                   DANGER ZONE                    *"))
    print(red("****************************************************"))
    if confirm(yellow("You are about to DELETE the whole database. Are you sure?"), default=False):
        _postgres(command="psql", pipe_in="-c \'DROP DATABASE;\'")


def logs(service=""):
    """
    Display logs
    :param service: Service to display the logs from. Default is all
    """
    docker_compose("logs" if not service else "logs {}".format(service))


def test():
    """
    Run a few test commands to check if the environment is setup correctly
    """
    # test that project dir is set
    if env.project_dir == "":
        print(red("You need to set env.project_dir, it is currently empty."))
        return

    with settings(warn_only=True):
        # test that the project dir exists
        if env.run("cd {}".format(env.project_dir)).return_code != 0:
            print(red("Your project directory '{}' does not exist on this machine. ".format(env.project_dir)))
            return

        # check that docker is installed
        if env.run("docker --version").return_code != 0:
            print(red("Can't run docker, is it installed?"))
            return

        # check that docker-compose is installed
        if env.run("docker-compose --version").return_code != 0:
            print(red("Can't run docker-compose, is it installed?"))
            return

        # check that git is installed
        if env.run("git --version").return_code != 0:
            print(red("Can't run git, is it installed?"))
            return

    print(green("I'm completely operational, and all my circuits are functioning perfectly."))


def docker_compose(command):
    """
    Run a docker-compose command
    :param command: Command you want to run
    """
    with env.cd(env.project_dir):
        return env.run("docker-compose -f {file} {command}".format(file=env.compose_file, command=command))


def _postgres(command=None, pipe_out="", pipe_in=""):
    remote_env = docker_compose("run postgres /bin/sh -c 'printenv'").stdout
    if not "POSTGRES_PORT_5432_TCP" in remote_env:
        print(red("Postgres commands can not be run on a stopped container, make sure the container is running"))
        return

    docker_compose(
        "run postgres /bin/sh -c '{password} {command} -h {host} -p {port} -U {user} -d {user} {pipe_in}' {pipe_out}".
            format(
                host="postgres",
                port="5432",
                user="$POSTGRES_USER" if "POSTGRES_USER" in remote_env else "postgres",
                password="export PGPASSWORD=$POSTGRES_PASSWORD;" if "POSTGRES_PASSWORD" in remote_env else "",
                command=command,
                pipe_out=pipe_out,
                pipe_in=pipe_in,
            )
    )