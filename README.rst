Cookiecutter Django
===================

.. image:: https://img.shields.io/github/workflow/status/cookiecutter/cookiecutter-django/CI/master
    :target: https://github.com/cookiecutter/cookiecutter-django/actions?query=workflow%3ACI
    :alt: Build Status

.. image:: https://readthedocs.org/projects/cookiecutter-django/badge/?version=latest
    :target: https://cookiecutter-django.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/cookiecutter/cookiecutter-django/shield.svg
    :target: https://pyup.io/repos/github/cookiecutter/cookiecutter-django/
    :alt: Updates

.. image:: https://img.shields.io/badge/Discord-cookiecutter-5865F2?style=flat&logo=discord&logoColor=white
    :target: https://discord.gg/bTfDa6Zz
    :alt: Join our Discord

.. image:: https://www.codetriage.com/cookiecutter/cookiecutter-django/badges/users.svg
    :target: https://www.codetriage.com/cookiecutter/cookiecutter-django
    :alt: Code Helpers Badge

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black

Powered by Cookiecutter_, Cookiecutter Django is a framework for jumpstarting
production-ready Django projects quickly.

* Documentation: https://cookiecutter-django.readthedocs.io/en/latest/
* See Troubleshooting_ for common errors and obstacles
* If you have problems with Cookiecutter Django, please open issues_ don't send
  emails to the maintainers.

.. _Troubleshooting: https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html

.. _528: https://github.com/cookiecutter/cookiecutter-django/issues/528#issuecomment-212650373
.. _issues: https://github.com/cookiecutter/cookiecutter-django/issues/new

Features
---------

* For Django 3.1
* Works with Python 3.9
* Renders Django projects with 100% starting test coverage
* Twitter Bootstrap_ v4 (`maintained Foundation fork`_ also available)
* 12-Factor_ based settings via django-environ_
* Secure by default. We believe in SSL.
* Optimized development and production settings
* Registration via django-allauth_
* Comes with custom user model ready to go
* Optional basic ASGI setup for Websockets
* Optional custom static build using Gulp and livereload
* Send emails via Anymail_ (using Mailgun_ by default or Amazon SES if AWS is selected cloud provider, but switchable)
* Media storage using Amazon S3 or Google Cloud Storage
* Docker support using docker-compose_ for development and production (using Traefik_ with LetsEncrypt_ support)
* Procfile_ for deploying to Heroku
* Instructions for deploying to PythonAnywhere_
* Run tests with unittest or pytest
* Customizable PostgreSQL version
* Default integration with pre-commit_ for identifying simple issues before submission to code review

.. _`maintained Foundation fork`: https://github.com/Parbhat/cookiecutter-django-foundation


Optional Integrations
---------------------

*These features can be enabled during initial project setup.*

* Serve static files from Amazon S3, Google Cloud Storage or Whitenoise_
* Configuration for Celery_ and Flower_ (the latter in Docker setup only)
* Integration with MailHog_ for local email testing
* Integration with Sentry_ for error logging

.. _Bootstrap: https://github.com/twbs/bootstrap
.. _django-environ: https://github.com/joke2k/django-environ
.. _12-Factor: http://12factor.net/
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _django-avatar: https://github.com/grantmcconnaughey/django-avatar
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Mailgun: http://www.mailgun.com/
.. _Whitenoise: https://whitenoise.readthedocs.io/
.. _Celery: http://www.celeryproject.org/
.. _Flower: https://github.com/mher/flower
.. _Anymail: https://github.com/anymail/django-anymail
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://sentry.io/welcome/
.. _docker-compose: https://github.com/docker/compose
.. _PythonAnywhere: https://www.pythonanywhere.com/
.. _Traefik: https://traefik.io/
.. _LetsEncrypt: https://letsencrypt.org/
.. _pre-commit: https://github.com/pre-commit/pre-commit

Constraints
-----------

* Only maintained 3rd party libraries are used.
* Uses PostgreSQL everywhere (10.16 - 13.2)
* Environment variables for configuration (This won't work with Apache/mod_wsgi).

Support this Project!
----------------------

This project is run by volunteers. Please support them in their efforts to maintain and improve Cookiecutter Django:

* Daniel Roy Greenfeld, Project Lead (`GitHub <https://github.com/pydanny>`_, `Patreon <https://www.patreon.com/danielroygreenfeld>`_): expertise in Django and AWS ELB.

* Nikita Shupeyko, Core Developer (`GitHub <https://github.com/webyneter>`_): expertise in Python/Django, hands-on DevOps and frontend experience.

Projects that provide financial support to the maintainers:



~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://cdn.shopify.com/s/files/1/0304/6901/products/Two-Scoops-of-Django-3-Alpha-Cover_540x_26507b15-e489-470b-8a97-02773dd498d1_1080x.jpg
   :name: Two Scoops of Django 3.x
   :align: center
   :alt: Two Scoops of Django
   :target: https://www.feldroy.com/products//two-scoops-of-django-3-x

Two Scoops of Django 3.x is the best ice cream-themed Django reference in the universe!

pyup
~~~~~~~~~~~~~~~~~~

.. image:: https://pyup.io/static/images/logo.png
   :name: pyup
   :align: center
   :alt: pyup
   :target: https://pyup.io/

Pyup brings you automated security and dependency updates used by Google and other organizations. Free for open source projects!

Usage
------

Let's pretend you want to create a Django project called "redditclone". Rather than using ``startproject``
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome::

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/cookiecutter/cookiecutter-django

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Daniel Greenfeld', 'pydanny', etc to your own information.

Answer the prompts with your own desired options_. For example::

    Cloning into 'cookiecutter-django'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    project_name [Project Name]: Reddit Clone
    project_slug [reddit_clone]: reddit
    author_name [Daniel Roy Greenfeld]: Daniel Greenfeld
    email [you@example.com]: pydanny@gmail.com
    description [Behold My Awesome Project!]: A reddit clone.
    domain_name [example.com]: myreddit.com
    version [0.1.0]: 0.0.1
    timezone [UTC]: America/Los_Angeles
    use_whitenoise [n]: n
    use_celery [n]: y
    use_mailhog [n]: n
    use_sentry [n]: y
    use_pycharm [n]: y
    windows [n]: n
    use_docker [n]: n
    use_heroku [n]: y
    use_compressor [n]: y
    Select postgresql_version:
    1 - 13.2
    2 - 12.6
    3 - 11.11
    4 - 10.16
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select js_task_runner:
    1 - None
    2 - Gulp
    Choose from 1, 2 [1]: 1
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 1
    custom_bootstrap_compilation [n]: n
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    keep_local_envs_in_vcs [y]: y
    debug[n]: n

Enter the project and take a look around::

    $ cd reddit/
    $ ls

Create a git repo and push it there::

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:pydanny/redditclone.git
    $ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?

For local development, see the following:

* `Developing locally`_
* `Developing locally using docker`_

.. _options: http://cookiecutter-django.readthedocs.io/en/latest/project-generation-options.html
.. _`Developing locally`: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html
.. _`Developing locally using docker`: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html

Community
-----------

* Have questions? **Before you ask questions anywhere else**, please post your question on `Stack Overflow`_ under the *cookiecutter-django* tag. We check there periodically for questions.
* If you think you found a bug or want to request a feature, please open an issue_.
* For anything else, you can chat with us on `Slack`_.

.. _`Stack Overflow`: http://stackoverflow.com/questions/tagged/cookiecutter-django
.. _`issue`: https://github.com/cookiecutter/cookiecutter-django/issues
.. _`Slack`: https://join.slack.com/t/cookie-cutter/shared_invite/enQtNzI0Mzg5NjE5Nzk5LTRlYWI2YTZhYmQ4YmU1Y2Q2NmE1ZjkwOGM0NDQyNTIwY2M4ZTgyNDVkNjMxMDdhZGI5ZGE5YmJjM2M3ODJlY2U

For Readers of Two Scoops of Django
--------------------------------------------

You may notice that some elements of this project do not exactly match what we describe in chapter 3. The reason for that is this project, amongst other things, serves as a test bed for trying out new ideas and concepts. Sometimes they work, sometimes they don't, but the end result is that it won't necessarily match precisely what is described in the book I co-authored.

For pyup.io Users
-----------------

If you are using `pyup.io`_ to keep your dependencies updated and secure, use the code *cookiecutter* during checkout to get 15% off every month.

.. _`pyup.io`: https://pyup.io

"Your Stuff"
-------------

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.

Releases
--------

Need a stable release? You can find them at https://github.com/cookiecutter/cookiecutter-django/releases


Not Exactly What You Want?
---------------------------

This is what I want. *It might not be what you want.* Don't worry, you have options:

Fork This
~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this to create your own version.
Once you have your fork working, let me know and I'll add it to a '*Similar Cookiecutter Templates*' list here.
It's up to you whether or not to rename your fork.

If you do rename your fork, I encourage you to submit it to the following places:

* cookiecutter_ so it gets listed in the README as a template.
* The cookiecutter grid_ on Django Packages.

.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _grid: https://www.djangopackages.com/grids/g/cookiecutters/

Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~

We accept pull requests if they're small, atomic, and make our own project development
experience better.

Articles
---------

* `Using cookiecutter-django with Google Cloud Storage`_ - Mar. 12, 2019
* `cookiecutter-django with Nginx, Route 53 and ELB`_ - Feb. 12, 2018
* `cookiecutter-django and Amazon RDS`_ - Feb. 7, 2018
* `Using Cookiecutter to Jumpstart a Django Project on Windows with PyCharm`_ - May 19, 2017
* `Exploring with Cookiecutter`_ - Dec. 3, 2016
* `Introduction to Cookiecutter-Django`_ - Feb. 19, 2016
* `Django and GitLab - Running Continuous Integration and tests with your FREE account`_ - May. 11, 2016
* `Development and Deployment of Cookiecutter-Django on Fedora`_ - Jan. 18, 2016
* `Development and Deployment of Cookiecutter-Django via Docker`_ - Dec. 29, 2015
* `How to create a Django Application using Cookiecutter and Django 1.8`_ - Sept. 12, 2015

Have a blog or online publication? Write about your cookiecutter-django tips and tricks, then send us a pull request with the link.

.. _`Using cookiecutter-django with Google Cloud Storage`: https://ahhda.github.io/cloud/gce/django/2019/03/12/using-django-cookiecutter-cloud-storage.html
.. _`cookiecutter-django with Nginx, Route 53 and ELB`: https://msaizar.com/blog/cookiecutter-django-nginx-route-53-and-elb/
.. _`cookiecutter-django and Amazon RDS`: https://msaizar.com/blog/cookiecutter-django-and-amazon-rds/
.. _`Exploring with Cookiecutter`: http://www.snowboardingcoder.com/django/2016/12/03/exploring-with-cookiecutter/
.. _`Using Cookiecutter to Jumpstart a Django Project on Windows with PyCharm`: https://joshuahunter.com/posts/using-cookiecutter-to-jumpstart-a-django-project-on-windows-with-pycharm/

.. _`Development and Deployment of Cookiecutter-Django via Docker`: https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-via-docker/
.. _`Development and Deployment of Cookiecutter-Django on Fedora`: https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-on-fedora/
.. _`How to create a Django Application using Cookiecutter and Django 1.8`: https://www.swapps.io/blog/how-to-create-a-django-application-using-cookiecutter-and-django-1-8/
.. _`Introduction to Cookiecutter-Django`: http://krzysztofzuraw.com/blog/2016/django-cookiecutter.html
.. _`Django and GitLab - Running Continuous Integration and tests with your FREE account`: http://dezoito.github.io/2016/05/11/django-gitlab-continuous-integration-phantomjs.html

Code of Conduct
---------------

Everyone interacting in the Cookiecutter project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.


.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
