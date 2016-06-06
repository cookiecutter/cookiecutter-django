FROM alpine
RUN  apk update
{% if cookiecutter.use_python2 == 'n' -%}
RUN  apk add bash python3 libpq && ln -s /usr/bin/python3 /usr/bin/python
RUN  pip3 install -U pip
{%- else %}
RUN  apk add bash python libpq curl
RUN  curl https://bootstrap.pypa.io/get-pip.py | python
{%- endif %}
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install -r /requirements/production.txt

RUN addgroup django && adduser -D -G django -s /sbin/nologin django
COPY . /app
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN sed -i 's/\r//' /gunicorn.sh
RUN chmod +x /entrypoint.sh && chown django /entrypoint.sh
RUN chmod +x /gunicorn.sh && chown django /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
