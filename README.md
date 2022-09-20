# Cookiecutter Django

[![Build Status](https://img.shields.io/github/workflow/status/cookiecutter/cookiecutter-django/CI/master)](https://github.com/cookiecutter/cookiecutter-django/actions?query=workflow%3ACI)
[![Documentation Status](https://readthedocs.org/projects/cookiecutter-django/badge/?version=latest)](https://cookiecutter-django.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/cookiecutter/cookiecutter-django/shield.svg)](https://pyup.io/repos/github/cookiecutter/cookiecutter-django/)
[![Join our Discord](https://img.shields.io/badge/Discord-cookiecutter-5865F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/uFXweDQc5a)
[![Code Helpers Badge](https://www.codetriage.com/cookiecutter/cookiecutter-django/badges/users.svg)](https://www.codetriage.com/cookiecutter/cookiecutter-django)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Cookiecutter Django is a framework for jumpstarting
production-ready Django projects quickly.

-   Documentation: <https://cookiecutter-django.readthedocs.io/en/latest/>
-   See [Troubleshooting](https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html) for common errors and obstacles
-   If you have problems with Cookiecutter Django, please open [issues](https://github.com/cookiecutter/cookiecutter-django/issues/new) don't send
    emails to the maintainers.

## Features

-   For Django 3.2
-   Works with Python 3.9
-   Renders Django projects with 100% starting test coverage
-   Twitter [Bootstrap](https://github.com/twbs/bootstrap) v5
-   [12-Factor](http://12factor.net/) based settings via [django-environ](https://github.com/joke2k/django-environ)
-   Secure by default. We believe in SSL.
-   Optimized development and production settings
-   Registration via [django-allauth](https://github.com/pennersr/django-allauth)
-   Comes with custom user model ready to go
-   Optional basic ASGI setup for Websockets
-   Optional custom static build using Gulp and livereload
-   Send emails via [Anymail](https://github.com/anymail/django-anymail) (using [Mailgun](http://www.mailgun.com/) by default or Amazon SES if AWS is selected cloud provider, but switchable)
-   Media storage using Amazon S3 or Google Cloud Storage
-   Docker support using [docker-compose](https://github.com/docker/compose) for development and production (using [Traefik](https://traefik.io/) with [LetsEncrypt](https://letsencrypt.org/) support)
-   [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to Heroku
-   Instructions for deploying to [PythonAnywhere](https://www.pythonanywhere.com/)
-   Run tests with unittest or pytest
-   Customizable PostgreSQL version
-   Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review

## Optional Integrations

*These features can be enabled during initial project setup.*

-   Serve static files from Amazon S3, Google Cloud Storage or [Whitenoise](https://whitenoise.readthedocs.io/)
-   Configuration for [Celery](https://docs.celeryq.dev) and [Flower](https://github.com/mher/flower) (the latter in Docker setup only)
-   Integration with [MailHog](https://github.com/mailhog/MailHog) for local email testing
-   Integration with [Sentry](https://sentry.io/welcome/) for error logging

## Constraints

-   Only maintained 3rd party libraries are used.
-   Uses PostgreSQL everywhere: 10.19 - 14.1 ([MySQL fork](https://github.com/mabdullahadeel/cookiecutter-django-mysql) also available).
-   Environment variables for configuration (This won't work with Apache/mod_wsgi).

## Support this Project!

This project is run by volunteers. Please support them in their efforts to maintain and improve Cookiecutter Django:

-   Daniel Roy Greenfeld, Project Lead ([GitHub](https://github.com/pydanny), [Patreon](https://www.patreon.com/danielroygreenfeld)): expertise in Django and AWS ELB.
-   Nikita Shupeyko, Core Developer ([GitHub](https://github.com/webyneter)): expertise in Python/Django, hands-on DevOps and frontend experience.

Projects that provide financial support to the maintainers:

------------------------------------------------------------------------

<p align="center">
  <a href="https://www.feldroy.com/products//two-scoops-of-django-3-x"><img src="https://cdn.shopify.com/s/files/1/0304/6901/products/Two-Scoops-of-Django-3-Alpha-Cover_540x_26507b15-e489-470b-8a97-02773dd498d1_1080x.jpg"></a>
</p>

Two Scoops of Django 3.x is the best ice cream-themed Django reference in the universe!

### PyUp

<p align="center">
  <a href="https://pyup.io/"><img src="https://pyup.io/static/images/logo.png"></a>
</p>

PyUp brings you automated security and dependency updates used by Google and other organizations. Free for open source projects!

## Usage

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get [cookiecutter](https://github.com/cookiecutter/cookiecutter) to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo:

    $ cookiecutter https://github.com/cookiecutter/cookiecutter-django

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Daniel Greenfeld', 'pydanny', etc to your own information.

Answer the prompts with your own desired [options](http://cookiecutter-django.readthedocs.io/en/latest/project-generation-options.html). For example:

    Cloning into 'cookiecutter-django'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    project_name [My Awesome Project]: Reddit Clone
    project_slug [reddit_clone]: reddit
    description [Behold My Awesome Project!]: A reddit clone.
    author_name [Daniel Roy Greenfeld]: Daniel Greenfeld
    domain_name [example.com]: myreddit.com
    email [daniel-greenfeld@example.com]: pydanny@gmail.com
    version [0.1.0]: 0.0.1
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    timezone [UTC]: America/Los_Angeles
    windows [n]: n
    use_pycharm [n]: y
    use_docker [n]: n
    Select postgresql_version:
    1 - 14
    2 - 13
    3 - 12
    4 - 11
    5 - 10
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 1
    Select mail_service:
    1 - Mailgun
    2 - Amazon SES
    3 - Mailjet
    4 - Mandrill
    5 - Postmark
    6 - Sendgrid
    7 - SendinBlue
    8 - SparkPost
    9 - Other SMTP
    Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 [1]: 1
    use_async [n]: n
    use_drf [n]: y
    Select frontend_pipeline:
    1 - None
    2 - Django Compressor
    3 - Gulp
    Choose from 1, 2, 3, 4 [1]: 1
    use_celery [n]: y
    use_mailhog [n]: n
    use_sentry [n]: y
    use_whitenoise [n]: n
    use_heroku [n]: y
    Select ci_tool:
    1 - None
    2 - Travis
    3 - Gitlab
    4 - Github
    Choose from 1, 2, 3, 4 [1]: 4
    keep_local_envs_in_vcs [y]: y
    debug [n]: n

Enter the project and take a look around:

    $ cd reddit/
    $ ls

Create a git repo and push it there:

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:pydanny/redditclone.git
    $ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?

For local development, see the following:

-   [Developing locally](http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html)
-   [Developing locally using docker](http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html)

## Community

-   Have questions? **Before you ask questions anywhere else**, please post your question on [Stack Overflow](http://stackoverflow.com/questions/tagged/cookiecutter-django) under the *cookiecutter-django* tag. We check there periodically for questions.
-   If you think you found a bug or want to request a feature, please open an [issue](https://github.com/cookiecutter/cookiecutter-django/issues).
-   For anything else, you can chat with us on [Discord](https://discord.gg/uFXweDQc5a).

## For Readers of Two Scoops of Django

You may notice that some elements of this project do not exactly match what we describe in chapter 3. The reason for that is this project, amongst other things, serves as a test bed for trying out new ideas and concepts. Sometimes they work, sometimes they don't, but the end result is that it won't necessarily match precisely what is described in the book I co-authored.

## For PyUp Users

If you are using [PyUp](https://pyup.io) to keep your dependencies updated and secure, use the code *cookiecutter* during checkout to get 15% off every month.

## "Your Stuff"

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.

## For MySQL users
To get full MySQL support in addition to the default Postgresql, you can use this fork of the cookiecutter-django:
https://github.com/mabdullahadeel/cookiecutter-django-mysql

## Releases

Need a stable release? You can find them at <https://github.com/cookiecutter/cookiecutter-django/releases>

## Not Exactly What You Want?

This is what I want. *It might not be what you want.* Don't worry, you have options:

### Fork This

If you have differences in your preferred setup, I encourage you to fork this to create your own version.
Once you have your fork working, let me know and I'll add it to a '*Similar Cookiecutter Templates*' list here.
It's up to you whether to rename your fork.

If you do rename your fork, I encourage you to submit it to the following places:

-   [cookiecutter](https://github.com/cookiecutter/cookiecutter) so it gets listed in the README as a template.
-   The cookiecutter [grid](https://www.djangopackages.com/grids/g/cookiecutters/) on Django Packages.

### Submit a Pull Request

We accept pull requests if they're small, atomic, and make our own project development
experience better.

## Articles

-   [Cookiecutter Django With Amazon RDS](https://haseeburrehman.com/posts/cookiecutter-django-with-amazon-rds/) - Apr, 2, 2021
-   [Using cookiecutter-django with Google Cloud Storage](https://ahhda.github.io/cloud/gce/django/2019/03/12/using-django-cookiecutter-cloud-storage.html) - Mar. 12, 2019
-   [cookiecutter-django with Nginx, Route 53 and ELB](https://msaizar.com/blog/cookiecutter-django-nginx-route-53-and-elb/) - Feb. 12, 2018
-   [cookiecutter-django and Amazon RDS](https://msaizar.com/blog/cookiecutter-django-and-amazon-rds/) - Feb. 7, 2018
-   [Using Cookiecutter to Jumpstart a Django Project on Windows with PyCharm](https://joshuahunter.com/posts/using-cookiecutter-to-jumpstart-a-django-project-on-windows-with-pycharm/) - May 19, 2017
-   [Exploring with Cookiecutter](http://www.snowboardingcoder.com/django/2016/12/03/exploring-with-cookiecutter/) - Dec. 3, 2016
-   [Introduction to Cookiecutter-Django](http://krzysztofzuraw.com/blog/2016/django-cookiecutter.html) - Feb. 19, 2016
-   [Django and GitLab - Running Continuous Integration and tests with your FREE account](http://dezoito.github.io/2016/05/11/django-gitlab-continuous-integration-phantomjs.html) - May. 11, 2016
-   [Development and Deployment of Cookiecutter-Django on Fedora](https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-on-fedora/) - Jan. 18, 2016
-   [Development and Deployment of Cookiecutter-Django via Docker](https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-via-docker/) - Dec. 29, 2015
-   [How to create a Django Application using Cookiecutter and Django 1.8](https://www.swapps.io/blog/how-to-create-a-django-application-using-cookiecutter-and-django-1-8/) - Sept. 12, 2015

Have a blog or online publication? Write about your cookiecutter-django tips and tricks, then send us a pull request with the link.
