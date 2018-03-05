Project Generation Options
==========================

project_name [My Awesome Project]:
    Your project's human-readable name, capitals and spaces allowed.

project_slug [my_awesome_project]:
    Your project's slug without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

description [Behold My Awesome Project!]
    Describes your project and gets used in places like `README.rst` and such.

author_name [Daniel Roy Greenfeld]:
    This is you! The value goes into places like `LICENSE` and such.

email [daniel-roy-greenfeld@example.com]:
    The email address you want to identify yourself in the project.

domain_name [example.com]
    The domain name you plan to use for your project ones it goes live.
    Note that it can be safely changed later on whenever you need to.

version [0.1.0]
    The version of the project at its inception.

open_source_license [1]
    A software license for the project. The choices are:

    1. MIT_
    2. BSD_
    3. GPLv3_
    4. `Apache Software License 2.0`_
    5. Not open source

timezone [UTC]
    The value to be used for the `TIME_ZONE` setting of the project.

windows [n]
    Indicates whether the project should be configured for development on Windows.

use_pycharm [n]
    Indicates whether the project should be configured for development with PyCharm_.

use_docker [y]
    Indicates whether the project should be configured to use Docker_ and `Docker Compose`_.

postgresql_version [1]
    Select a PostgreSQL_ version to use. The choices are:

    1. 10.3
    2. 10.2
    3. 10.1
    4. 9.6
    5. 9.5
    6. 9.4
    7. 9.3

js_task_runner [1]
    Select a JavaScript task runner. The choices are:

    1. Gulp_
    2. Grunt_
    3. None

custom_bootstrap_compilation [n]
    Indicates whether the project should support Bootstrap recompilation
    via the selected JavaScript task runner's task. This can be useful
    for real-time Bootstrap variable alteration.

use_compressor [n]
    Indicates whether the project should be configured to use `Django Compressor`_.

use_celery [n]
    Indicates whether the project should be configured to use Celery_.

use_mailhog [n]
    Indicates whether the project should be configured to use MailHog_.

use_sentry_for_error_reporting [n]
    Indicates whether the project should be configured to use Sentry_.

use_opbeat [n]
    Indicates whether the project should be configured to use Opbeat_.

use_whitenoise [y]
    Indicates whether the project should be configured to use WhiteNoise_.

use_heroku [n]
    Indicates whether the project should be configured so as to be deployable
    to Heroku_.

use_travisci [n]
    Indicates whether the project should be configured to use `Travis CI`_.


.. _MIT: https://opensource.org/licenses/MIT
.. _BSD: https://opensource.org/licenses/BSD-3-Clause
.. _GPLv3: https://www.gnu.org/licenses/gpl.html
.. _Apache Software License 2.0: http://www.apache.org/licenses/LICENSE-2.0

.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _Docker: https://github.com/docker/docker
.. _Docker Compose: https://docs.docker.com/compose/

.. _PostgreSQL: https://www.postgresql.org/docs/

.. _Gulp: https://github.com/gulpjs/gulp
.. _Grunt: https://github.com/gruntjs/grunt

.. _Django Compressor: https://github.com/django-compressor/django-compressor

.. _Celery: https://github.com/celery/celery

.. _MailHog: https://github.com/mailhog/MailHog

.. _Sentry: https://github.com/getsentry/sentry

.. _Opbeat: https://github.com/opbeat/opbeat_python

.. _WhiteNoise: https://github.com/evansd/whitenoise

.. _Heroku: https://github.com/heroku/heroku-buildpack-python

.. _Travis CI: https://travis-ci.org/
