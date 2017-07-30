#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

rm -f './celerybeat.pid'
celery -A {{cookiecutter.project_slug}}.taskapp beat -l INFO
