#!/bin/bash

set -o errexit
set -o nounset


celery -A config.celery_app worker -l INFO
