.. _template-options:

Project Generation Options
==========================

This page describes all the template options that will be prompted by the `cookiecutter CLI`_ prior to generating your project.

.. _cookiecutter CLI: https://github.com/cookiecutter/cookiecutter

project_name:
    Your project's human-readable name, capitals and spaces allowed.

project_slug:
    Your project's slug without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

description:
    Describes your project and gets used in places like ``README.rst`` and such.

author_name:
    This is you! The value goes into places like ``LICENSE`` and such.

email:
    The email address you want to identify yourself in the project.

domain_name:
    The domain name you plan to use for your project once it goes live.
    Note that it can be safely changed later on whenever you need to.

version:
    The version of the project at its inception.

open_source_license:
    A software license for the project. The choices are:

    1. MIT_
    2. BSD_
    3. GPLv3_
    4. `Apache Software License 2.0`_
    5. Not open source

timezone:
    The value to be used for the ``TIME_ZONE`` setting of the project.

windows:
    Indicates whether the project should be configured for development on Windows.

use_pycharm:
    Indicates whether the project should be configured for development with PyCharm_.

use_docker:
    Indicates whether the project should be configured to use Docker_ and `Docker Compose`_.

postgresql_version:
    Select a PostgreSQL_ version to use. The choices are:

    1. 14.1
    2. 13.5
    3. 12.9
    4. 11.14
    5. 10.19

js_task_runner:
    Select a JavaScript task runner. The choices are:

    1. None
    2. Gulp_

cloud_provider:
    Select a cloud provider for static & media files. The choices are:

    1. AWS_
    2. GCP_
    3. None

    Note that if you choose no cloud provider, media files won't work.

mail_service:
    Select an email service that Django-Anymail provides

    1. Mailgun_
    2. `Amazon SES`_
    3. Mailjet_
    4. Mandrill_
    5. Postmark_
    6. SendGrid_
    7. SendinBlue_
    8. SparkPost_
    9. `Other SMTP`_

use_async:
    Indicates whether the project should use web sockets with Uvicorn + Gunicorn.

use_drf:
    Indicates whether the project should be configured to use `Django Rest Framework`_.

custom_bootstrap_compilation:
    Indicates whether the project should support Bootstrap recompilation
    via the selected JavaScript task runner's task. This can be useful
    for real-time Bootstrap variable alteration.

use_compressor:
    Indicates whether the project should be configured to use `Django Compressor`_.

use_celery:
    Indicates whether the project should be configured to use Celery_.

use_mailhog:
    Indicates whether the project should be configured to use MailHog_.

use_sentry:
    Indicates whether the project should be configured to use Sentry_.

use_whitenoise:
    Indicates whether the project should be configured to use WhiteNoise_.

use_heroku:
    Indicates whether the project should be configured so as to be deployable
    to Heroku_.

ci_tool:
    Select a CI tool for running tests. The choices are:

    1. None
    2. `Travis CI`_
    3. `Gitlab CI`_
    4. `Github Actions`_

keep_local_envs_in_vcs:
    Indicates whether the project's ``.envs/.local/`` should be kept in VCS
    (comes in handy when working in teams where local environment reproducibility
    is strongly encouraged).
    Note: .env(s) are only utilized when Docker Compose and/or Heroku support is enabled.

debug:
    Indicates whether the project should be configured for debugging.
    This option is relevant for Cookiecutter Django developers only.


.. _MIT: https://opensource.org/licenses/MIT
.. _BSD: https://opensource.org/licenses/BSD-3-Clause
.. _GPLv3: https://www.gnu.org/licenses/gpl.html
.. _Apache Software License 2.0: http://www.apache.org/licenses/LICENSE-2.0

.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _Docker: https://github.com/docker/docker
.. _Docker Compose: https://docs.docker.com/compose/

.. _PostgreSQL: https://www.postgresql.org/docs/

.. _Gulp: https://github.com/gulpjs/gulp

.. _AWS: https://aws.amazon.com/s3/
.. _GCP: https://cloud.google.com/storage/

.. _Amazon SES: https://aws.amazon.com/ses/
.. _Mailgun: https://www.mailgun.com
.. _Mailjet: https://www.mailjet.com
.. _Mandrill: http://mandrill.com
.. _Postmark: https://postmarkapp.com
.. _SendGrid: https://sendgrid.com
.. _SendinBlue: https://www.sendinblue.com
.. _SparkPost: https://www.sparkpost.com
.. _Other SMTP: https://anymail.readthedocs.io/en/stable/

.. _Django Rest Framework: https://github.com/encode/django-rest-framework/

.. _Django Compressor: https://github.com/django-compressor/django-compressor

.. _Celery: https://github.com/celery/celery

.. _MailHog: https://github.com/mailhog/MailHog

.. _Sentry: https://github.com/getsentry/sentry

.. _WhiteNoise: https://github.com/evansd/whitenoise

.. _Heroku: https://github.com/heroku/heroku-buildpack-python

.. _Travis CI: https://travis-ci.org/

.. _GitLab CI: https://docs.gitlab.com/ee/ci/

.. _Github Actions: https://docs.github.com/en/actions
