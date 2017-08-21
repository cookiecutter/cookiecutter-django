Support Matrix
==============

.. index:: matrix, support matrix, compatibility matrix, version matrix, version support matrix



Scope
-----


Setups
~~~~~~

* **Bare bones**: native Python setup implying the use of `virtualenv`_ and friends (`pyenv`_, `pyenv-virtualenv`_, `virtualenvwrapper`_, `pyenv-virtualenvwrapper`_, `pipenv`_ etc.)
* **Docker**: Docker-powered setup implying the use of `Docker`_, `Docker Compose`_ etc.

.. _`virtualenv`: https://github.com/pypa/virtualenv
.. _`pyenv`: https://github.com/pyenv/pyenv
.. _`pyenv-virtualenv`: https://github.com/pyenv/pyenv-virtualenv
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/stable/
.. _`pyenv-virtualenvwrapper`: https://github.com/pyenv/pyenv-virtualenvwrapper
.. _`pipenv`: https://github.com/kennethreitz/pipenv
.. _`Docker`: https://github.com/moby/moby
.. _`Docker Compose`: https://github.com/docker/compose


Operating Systems
~~~~~~~~~~~~~~~~~

* **Linux**.
* **Mac**.
* **Windows**.


Notation
~~~~~~~~

* +: supported.
* ⌚: soon to be supported.
* −: not supported.



Environments
------------

.. Generated via http://www.tablesgenerator.com/text_tables
.. Header rows and columns' thick borders set manually.


Development
~~~~~~~~~~~

+---------------+-----------------------+-----------------------+
|               |       Bare bones      |         Docker        |
+---------------+-----------------------+-----------------------+
|               | Linux | Mac | Windows | Linux | Mac | Windows |
+===============+=======+=====+=========+=======+=====+=========+
| `WhiteNoise`_ |       |     |         |   \+  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `Celery`_     |       |     |         |   \+  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `MailHog`_    |       |     |         |   \+  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `Sentry`_     |       |     |         |   \+  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `Opbeat`_     |       |     |         |   \+  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `Compressor`_ |       |     |         |   \+  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `Gulp`_       |       |     |         |   \⌚  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `Grunt`_      |       |     |         |   \−  |     |         |
+---------------+-------+-----+---------+-------+-----+---------+
| `PyCharm`_    |                       \+                      |
+---------------+-----------------------------------------------+


Production
~~~~~~~~~~



.. Elastic Beanstalk \*: experimental support.


.. _`PostgreSQL`: https://www.postgresql.org/
.. _`WhiteNoise`: https://github.com/evansd/whitenoise
.. _`Celery`: https://github.com/celery/celery
.. _`MailHog`: https://github.com/mailhog/MailHog
.. _`Sentry`: https://github.com/getsentry/sentry
.. _`Opbeat`: https://github.com/opbeat/opbeat_python
.. _`Compressor`: https://github.com/django-compressor/django-compressor
.. _`Gulp`: https://github.com/gulpjs/gulp
.. _`Grunt`: https://github.com/gruntjs/grunt
.. _`Heroku`: https://www.heroku.com/
.. _`Elastic Beanstalk`: https://aws.amazon.com/elasticbeanstalk/
.. _`PyCharm`: https://www.jetbrains.com/pycharm/
