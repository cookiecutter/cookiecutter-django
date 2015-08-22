FROM cookiecutterdjango/base

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements /requirements
ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN pip install -r /requirements/local.txt

ADD . /app

WORKDIR /app

ENTRYPOINT ["/app/compose/django/entrypoint.sh"]
