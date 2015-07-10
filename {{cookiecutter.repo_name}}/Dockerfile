# Only intended for development purposes.
# For production deployment options, see the Deployment section in
# README.rst

FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/local.txt
