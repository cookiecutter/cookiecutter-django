FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN groupadd -r django && useradd -r -g django django

RUN apt-get update
RUN apt-get -y install libmemcached-dev

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements /requirements
ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN pip install -r /requirements/local.txt

ADD . /app

ADD ./compose/django/gunicorn.sh /gunicorn.sh
ADD ./compose/django/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
RUN chmod +x /gunicorn.sh

RUN chown -R django /app

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]