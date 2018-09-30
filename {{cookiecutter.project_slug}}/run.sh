#!/bin/bash
set -e
export NEW_RELIC_CONFIG_FILE=$(/usr/local/bin/envconsul  -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ env | grep ^NEW_RELIC_CONFIG_FILE= | cut -d = -f2 | awk '{print $1 }')


if [ "$1" = "{{ cookiecutter.project_slug }}" ]; then
  echo "Running {{ cookiecutter.project_slug }}"
  /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
    python manage.py migrate

  /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
    python manage.py loaddata seed_data.json

  /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
    python manage.py collectstatic --noinput

  if [ -z "$NEW_RELIC_CONFIG_FILE" ] ; then
    /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
      python manage.py runserver 0.0.0.0:8000
  else
    /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ python newrelic-customizer.py
    /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
     newrelic-admin run-program python manage.py runserver 0.0.0.0:8000
  fi

elif [ "$1" = "worker" ]; then
  echo "Running celery worker"

  if [ -z "$NEW_RELIC_CONFIG_FILE" ] ; then
    /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
      celery worker -A walla --loglevel=INFO -Q {{ cookiecutter.project_slug }}
  else
    /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ python newrelic-customizer.py --postfix "worker"
    /usr/local/bin/envconsul -consul consul.mcagrid.com -token $CONSUL_TOKEN -prefix $DEPLOY_ENV/ \
      newrelic-admin run-program celery worker -A walla --loglevel=INFO -Q {{ cookiecutter.project_slug }}
  fi
fi