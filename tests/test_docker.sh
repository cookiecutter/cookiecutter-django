#!/bin/sh

pip install -r requirements/production.txt

mkdir -p .cache/docker
cd .cache/docker

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ \
    --no-input \
    --overwrite-if-exists use_docker=y
cd project_name

docker-compose -f local.yml run --rm django pytest

docker-compose -f local.yml run --rm django python manage.py makemigrations --dry-run --check || { echo "ERROR: there were changes in the models, but migration listed above have not been created and are not saved in version control"; exit 1; }
