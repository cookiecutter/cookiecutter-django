Project Generation Options
==========================

project_name [project_name]:
    Your human-readable project name, including any capitalization or spaces.

project_slug [project_name]:
    The slug of your project, without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

author_name [Your Name]:
    You! This goes into places like the LICENSE file.

email [Your email]:
    Your email address.

description [A short description of the project.]
    Used in the generated README.rst and other places.

domain_name [example.com]
    Whatever domain name you plan to use for your project when it goes live.

version [0.1.0]
    The starting version number for your project.

timezone [UTC]
    Used in the common settings file for the `TIME_ZONE` value.

use_whitenoise [y]
    Whether to use WhiteNoise_ for static file serving.

use_celery [n]
    Whether to use Celery_. This gives you the ability to use distributed task
    queues in your project.

use_mailhog [n]
    Whether to use MailHog_. MailHog is a tool that simulates email receiving
    for development purposes. It runs a simple SMTP server which catches
    any message sent to it. Messages are displayed in a web interface which runs at ``http://localhost:8025/`` You need to download the MailHog executable for your operating system, see `Getting Up and Running Locally`_ for instructions.

use_sentry_for_error_reporting [y]
    Whether to use Sentry_ to log errors from your project.
    
use_opbeat [n]
    Whether to support Opbeat_ for performance monitoring.

use_pycharm [n]
    Whether you'll be using PyCharm_ to edit your code.

windows [n]
    Whether you'll be developing on Windows.

use_python2 [n]
    By default, the Python code generated will be for Python 3.x. But if you
    answer `y` here, it will be legacy Python 2.7 code.
    
use_docker [y]
    Whether to use Docker_. See `Getting Up and Running Locally With Docker`_ and `Deployment with Docker`_ for instructions.
    
use_heroku [n]
    Whether to use Heroku_ for deployment. See `Deployment on Heroku`_ for instructions.

use_compressor [n]
    Whether to use `Django Compressor`_ to compress linked and inline JavaScript or CSS into a single cached file.

js_task_runner [1]
    Select a JavaScript task runner:

    1. Gulp
    2. Grunt
    3. Webpack
    4. None

use_lets_encrypt [n]
    If using Docker_, enable https support using `Let's Encrypt`_.

open_source_license [1]
    Select a license for your project:
    
    1. MIT
    2. BSD
    3. GPLv3
    4. Apache Software License 2.0
    5. Not open source
    
.. _WhiteNoise: https://github.com/evansd/whitenoise
.. _Celery: https://github.com/celery/celery
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://github.com/getsentry/sentry
.. _Getting Up and Running Locally: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html
.. _Getting Up and Running Locally With Docker: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html
.. _Deployment with Docker: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
.. _Deployment on Heroku: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _Let's Encrypt: https://letsencrypt.org/
.. _Opbeat: https://opbeat.com/
.. _Heroku: https://www.heroku.com/
.. _Docker: https://www.docker.com/
.. _Django Compressor: https://django-compressor.readthedocs.io/en/latest/
