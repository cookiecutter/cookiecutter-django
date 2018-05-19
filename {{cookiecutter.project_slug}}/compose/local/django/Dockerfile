FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update
Run apt install -y binutils libproj-dev gdal-bin

RUN apt-get update 
  # psycopg2 dependencies
RUN apt install -y build-essential gcc python3-dev musl-dev 
  # Pillow dependencies
  # && apt install -y tk-dev tcl-dev \
  # CFFI dependencies
# RUN apt install -y openssl-dev 
  # Translations dependencies
RUN apt install -y gettext 
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
RUN apt install -y postgresql-client



# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/local/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
