FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
{%- if cookiecutter.use_watchman == "y" %}
  # needed to download watchman
  && apt-get install -y curl unzip \
{%- endif %}
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

{%- if cookiecutter.use_watchman == "y" %}
ARG WATCHMAN_VERSION=v2021.03.01.00
WORKDIR /watchman-build
RUN curl -sSLO https://github.com/facebook/watchman/releases/download/${WATCHMAN_VERSION}/watchman-${WATCHMAN_VERSION}-linux.zip && \
    unzip watchman-${WATCHMAN_VERSION}-linux.zip && \
    chmod +x watchman-${WATCHMAN_VERSION}-linux/bin/* \
      watchman-${WATCHMAN_VERSION}-linux/lib/* && \
    cp -rp watchman-${WATCHMAN_VERSION}-linux/bin/* /usr/local/bin/ && \
    cp -rp watchman-${WATCHMAN_VERSION}-linux/lib/* /usr/local/lib/ && \
    mkdir -p /usr/local/var/run/watchman && chown 2777 /usr/local/var/run/watchman
# The pywatchman version on pypi is really outdated, build from source
RUN curl -sSLO https://github.com/facebook/watchman/archive/refs/tags/${WATCHMAN_VERSION}.zip && \
    unzip ${WATCHMAN_VERSION}.zip && cd watchman-*/python && \
    python setup.py bdist_wheel && \
    pip install dist/pywatchman*whl
WORKDIR /
RUN rm -rf /watchman-build
{%- endif %}

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
{% if cookiecutter.use_celery == "y" %}
COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower
{% endif %}
WORKDIR /app

ENTRYPOINT ["/entrypoint"]
