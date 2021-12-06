#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_bare.sh

set -o errexit
set -x

# Install modern pip with new resolver:
# https://blog.python.org/2020/11/pip-20-3-release-new-resolver.html
pip install 'pip>=20.3'

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

# Lint by running pre-commit on all files
# Needs a git repo to find the project root
git init
git add .
pre-commit run --show-diff-on-failure -a

# run the project's tests
pytest

if [ -f "package.json" ]
then
    npm install
    if [ -f "gulpfile.js" ]
    then
        npm run build
    fi
fi

