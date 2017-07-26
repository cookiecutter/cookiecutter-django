#!/usr/bin/env python

"""
# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.
"""

from __future__ import print_function
import os
import sys
import psycopg2
import time


def exports(**kwargs):
    """Useful environment variables
    :list: TODO
    """
    os.environ['REDIS_URL'] = 'redis://redis:6379'
    os.environ['CELERY_BROKER_URL'] = os.environ['REDIS_URL'] + '/0'

def pingpost():
    """
    This is the function that actually trys to connect
    to postgres
    """
    try:
        if os.environ['POSTGRES_USER']:
            pg_user = os.environ['POSTGRES_USER']
        else:
            os.environ['POSTGRES_USER'] = pg_user = 'postgres'

        try:
            pg_pass = os.environ['POSTGRES_PASSWORD']
        except Exception as e:
            pg_pass = ''

        DATABASE_URL='postgres://{username}:{password}@postgres:5432/{username}'
        DATABASE_URL = DATABASE_URL.format(username=pg_user, password=pg_pass)
        os.environ['DATABASE_URL'] = DATABASE_URL

        conn = psycopg2.connect(DATABASE_URL, connect_timeout=3)

    except psycopg2.OperationalError as error:
        print(error)
        return False
    return True

def main(arguments):
    """
    call exports
    and check to see if postgres is ready
    """
    exports()

    while True:
        if pingpost():
            break
            print('Postgres is unavailable - sleeping')
            time.sleep(1)

    import subprocess
    try:
        hold = subprocess.check_call(arguments)
    except subprocess.CalledProcessError as cpe:
        print("something went wrong")
        raise Exception(cpe)

    print('exiting: ...')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
