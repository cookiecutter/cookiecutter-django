#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

celery -A {{cookiecutter.project_slug}}.taskapp worker -l INFO
