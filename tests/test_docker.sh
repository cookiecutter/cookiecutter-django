#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_docker.sh

set -o errexit

# install test requirements
pip install -r requirements.txt

# create a cache directory
mkdir -p .cache/docker
cd .cache/docker

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ --no-input --overwrite-if-exists use_docker=y $@
cd my_awesome_project

# run migrations
docker-compose -f local.yml run django python manage.py migrate

# view backups
docker-compose -f local.yml exec postgres backups

