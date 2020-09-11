{% if cookiecutter.js_task_runner == 'Gulp' -%}
FROM node:10-stretch-slim as client-builder

WORKDIR /app
COPY ./package.json /app
RUN npm install && npm cache clean --force
COPY . /app
RUN npm run build

{%- endif %}

# Python build stage
FROM python:3.8-slim-buster as python-build-stage


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  # create python dependency wheels
  && pip wheel --no-cache-dir --no-deps --use-feature=2020-resolver --wheel-dir /usr/src/app/wheels -r /requirements/production.txt \
  && rm -rf /requirements


# Python 'run' stage
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


{%- if cookiecutter.use_celery == "y" %}
COPY --chown=django:django ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


COPY --chown=django:django ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat


COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower
{%- endif %}

# installing required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels

# install python dependencies
RUN pip install --no-cache /wheels/*

{%- if cookiecutter.js_task_runner == 'Gulp' %}
COPY --from=client-builder --chown=django:django /app /app
{% else %}
COPY --chown=django:django . /app
{%- endif %}

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
