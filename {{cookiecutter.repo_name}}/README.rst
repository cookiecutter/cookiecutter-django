{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}


LICENSE: MIT

Deployment
------------

* heroku create
* heroku addons:add heroku-postgresql:dev
* heroku addons:add pgbackups
* heroku addons:add sendgrid:starter
* heroku pg:promote HEROKU_POSTGRESQL_COLOR
* heroku config:add AWS_ACCESS_KEY_ID=YOUR_ID
* heroku config:add AWS_SECRET_ACCESS_KEY=YOUR_KEY
* heroku config:add AWS_STORAGE_BUCKET_NAME=BUCKET
* git push heroku master
* heroku run python {{cookiecutter.repo_name}}/manage.py syncdb --noinput --settings=config.settings
* heroku run python {{cookiecutter.repo_name}}/manage.py migrate --settings=config.settings
* heroku run python {{cookiecutter.repo_name}}/manage.py collectstatic --settings=config.settings

Run this script: (TODO - automate this)

.. code-block:: python

    from django.contrib.sites.models import Site
    site = Site.objects.get()
    site.domain = "{{cookiecutter.project_name}}.com"
    site.name = "{{cookiecutter.project_name}}"
    site.save()
