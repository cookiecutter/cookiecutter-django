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
    any message sent to it. Messages are displayed in a web interface which runs at ``http://localhost:8025/`` You need to download the MailHog executable for your operating system, see the 'Developing Locally' docs for instructions.

use_sentry [n]
    Whether to use Sentry_ to log errors from your project.

windows [n]
    Whether you'll be developing on Windows.

use_python2 [n]
    By default, the Python code generated will be for Python 3.x. But if you
    answer `y` here, it will be legacy Python 2.7 code.

.. _WhiteNoise: https://github.com/evansd/whitenoise
.. _Celery: https://github.com/celery/celery
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://github.com/getsentry/sentry
