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
    Used in the base settings file for the `TIME_ZONE` value.

use_whitenoise [y]
    Whether to use WhiteNoise_ for static file serving.

use_celery [n]
    Whether to use Celery_. This gives you the ability to use distributed task
    queues in your project.

use_mailhog [n]
    Whether to use MailHog_. MailHog is a tool that simulates email receiving
    for development purposes. It runs a simple SMTP server which catches
    any message sent to it. Messages are displayed in a web interface which
    runs at ``http://localhost:8025/`` You need to download the MailHog
    executable for your operating system, see the 'Developing Locally' docs
    for instructions.

use_sentry_for_error_reporting [n]
    Whether to use Sentry_ to log errors from your project.

use_opbeat [n]
    Whether to use Opbeat_ for preformance monitoring and code optimization.

use_pycharm [n]
    Adds support for developing in PyCharm_ with a preconfigured .idea directory.

windows [n]
    Whether you'll be developing on Windows.

use_docker [y]
    Whether to use Docker_, separating the app and database into separate
    containers.

use_heroku [n]
    Add configuration to deploy the application to a Heroku_ instance.

use_compressor [n]
    Use `Django Compressor`_ to minify and combine rendered JavaScript and CSS
    into cachable static resources.

js_task_runner [1]
    Select a JavaScript task runner. The choices are:

    1. Gulp_
    2. Grunt_
    3. None

custom_bootstrap_compilation [n]
    If you use Grunt, scaffold out recompiling Bootstrap as as task.  (Useful for letting you change Bootstrap variables in real time.)  Consult project README for more details.

open_source_license [1]
    Select a software license for the project. The choices are:

    1. MIT_
    2. BSD_
    3. GPLv3_
    4. `Apache Software License 2.0`_
    5. Not open source

**NOTE:** *If you choose to use Docker, selecting a JavaScript task runner is
not supported out of the box.*

.. _WhiteNoise: https://github.com/evansd/whitenoise
.. _Celery: https://github.com/celery/celery
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://github.com/getsentry/sentry
.. _Opbeat: https://github.com/opbeat/opbeat_python
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _Docker: https://github.com/docker/docker
.. _Heroku: https://github.com/heroku/heroku-buildpack-python
.. _Django Compressor: https://github.com/django-compressor/django-compressor
.. _Gulp: https://github.com/gulpjs/gulp
.. _Grunt: https://github.com/gruntjs/grunt
.. _Webpack: https://github.com/webpack/webpack
.. _Let's Encrypt: https://github.com/certbot/certbot
.. _MIT: https://opensource.org/licenses/MIT
.. _BSD: https://opensource.org/licenses/BSD-3-Clause
.. _GPLv3: https://www.gnu.org/licenses/gpl.html
.. _Apache Software License 2.0: http://www.apache.org/licenses/LICENSE-2.0
