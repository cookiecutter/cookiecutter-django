#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


celery -A {{cookiecutter.project_slug}}.taskapp worker -l INFO
