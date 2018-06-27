FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

ARG environment

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  && [ "${environment}" != 'production' ] && apk add \
    # Translations dependencies
    gettext \
    # and https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
    postgresql-client

COPY ./requirements/ /app/requirements/
WORKDIR /app/
RUN [ "${environment}" = 'production' ] && pip --no-cache-dir install -r "./requirements/${environment}.txt" || pip install -r "./requirements/${environment}.txt"

RUN addgroup -S django \
    && adduser -S -g django django

COPY ./docker/django/scripts/ /scripts/
RUN [ "${environment}" = 'production' ] && find /scripts/ -type f -name '*.local' -exec rm -f {} \; || true
RUN chown --recursive django:django /scripts/
RUN find /scripts/ -type f -exec sed -i 's/\r//' {} \;
RUN chmod +x /scripts/*
RUN mv /scripts/* / \
    && rmdir /scripts/

COPY . /app/
RUN chown --recursive django:django /app/

USER django

ENTRYPOINT ["/entrypoint"]

ARG cmd
# See why we need ENV as well: https://stackoverflow.com/a/35562189
ENV cmd ${cmd}
CMD ${cmd}
