#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_docker.sh

set -o errexit
set -x

# install test requirements
pip install -r requirements.txt

# create a cache directory
mkdir -p .cache/docker
cd .cache/docker

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ --no-input --overwrite-if-exists use_docker=y $@
cd my_awesome_project

# Lint by running pre-commit on all files
# Needs a git repo to find the project root
# We don't have git inside Docker, so run it outside
git init
git add .
pre-commit run --show-diff-on-failure -a

# run the project's type checks
docker-compose -f local.yml run django mypy my_awesome_project

# run the project's tests
docker-compose -f local.yml run django pytest

# return non-zero status code if there are migrations that have not been created
docker-compose -f local.yml run django python manage.py makemigrations --dry-run --check || { echo "ERROR: there were changes in the models, but migration listed above have not been created and are not saved in version control"; exit 1; }

# Test support for translations
docker-compose -f local.yml run django python manage.py makemessages --all
