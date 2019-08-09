#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_docker.sh

set -o errexit

# install test requirements
pip install -r requirements.txt

# create a cache directory
mkdir -p .cache/bare
cd .cache/bare

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ --no-input --overwrite-if-exists use_docker=n $@
cd my_awesome_project

# Install OS deps
sudo utility/install_os_dependencies.sh install

# Install Python deps
pip install -r requirements/local.txt

# run the project's tests
pytest
