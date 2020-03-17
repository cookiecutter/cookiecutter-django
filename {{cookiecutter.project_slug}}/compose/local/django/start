#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py migrate
python manage.py runserver_plus 0.0.0.0:8000
