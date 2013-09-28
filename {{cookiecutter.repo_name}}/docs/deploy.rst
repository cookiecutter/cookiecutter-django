Deploy
========

From within your project's directory, run this command to create a Heroku app::

	$ heroku create {{cookiecutter.project_name}}
	Creating {{cookiecutter.project_name}}... done, stack is cedar
	http://{{cookiecutter.project_name}}.herokuapp.com/ | git@heroku.com:{{cookiecutter.project_name}}.git

If you haven't cloned the project from an existing git repo, then you need to initialize it::

	$ cd {{cookiecutter.repo_name}}
	$ git init
	Initialized empty Git repository in /path/to/your/project/{{cookiecutter.repo_name}}/.git/

Add the Heroku git repo as a remote, so that we can push to it.

	$ git remote add heroku git@heroku.com:{{cookiecutter.project_name}}.git

Add a PostgreSQL database. Note that you will probably get a color other than "GOLD". This is normal.

	$ heroku addons:add heroku-postgresql:dev
	Adding heroku-postgresql:dev on {{cookiecutter.project_name}}... done, v3 (free)
	Attached as HEROKU_POSTGRESQL_GOLD_URL
	Database has been created and is available
 	! This database is empty. If upgrading, you can transfer
 	! data from another database with pgbackups:restore.

Add pgbackups to handle backups of the PostgreSQL database::

	$ heroku addons:add pgbackups
	Adding pgbackups on {{cookiecutter.project_name}}... done, v4 (free)
	You can now use "pgbackups" to backup your databases or import an external backup.
	Use `heroku addons:docs pgbackups` to view documentation.

Add sendgrid to handle the sending of emails::

	$ heroku addons:add sendgrid:starter
	Adding sendgrid:starter on {{cookiecutter.project_name}}... done, v5 (free)
	Use `heroku addons:docs sendgrid` to view documentation.

Add memcachier for memcached service::

	$ heroku addons:add memcachier:dev
	Adding memcachier:dev on {{cookiecutter.project_name}}... done, v7 (free)
	MemCachier is now up and ready to go. Happy bananas!
	Use `heroku addons:docs memcachier` to view documentation.

Promote the database you just created. Please note that your database might be called something other than "GOLD"::

	$ heroku pg:promote HEROKU_POSTGRESQL_GOLD
	Promoting HEROKU_POSTGRESQL_GOLD_URL to DATABASE_URL... done

Set the DJANGO_CONFIGURATION environment variable so that Heroku knows we're in production::

	$ heroku config:add DJANGO_CONFIGURATION=Production
	Setting config vars and restarting {{cookiecutter.project_name}}... done, v8
	DJANGO_CONFIGURATION: Production

Don't forget to replace the secret key with a random string::

	$ heroku config:add DJANGO_SECRET_KEY='!!!REPLACE-ME!!!'
	Setting config vars and restarting {{cookiecutter.project_name}}... done, v9
	DJANGO_SECRET_KEY: abcdefghijklmnopqrstuvwxyz

If you're using AWS S3 to serve up static assets, then you need to set these values::

	$ heroku config:add DJANGO_AWS_ACCESS_KEY_ID=YOUR_ID
	$ heroku config:add DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_KEY
	$ heroku config:add DJANGO_AWS_STORAGE_BUCKET_NAME=BUCKET

Commit all the files in your project, and now we're finally ready to push the code to Heroku!::

	$ git commit -a
	$ git push heroku master
	Counting objects: 75, done.
	Delta compression using up to 8 threads.
	Compressing objects: 100% (67/67), done.
	Writing objects: 100% (75/75), 28.12 KiB, done.
	Total 75 (delta 4), reused 0 (delta 0)

	-----> Python app detected
	-----> No runtime.txt provided; assuming python-2.7.4.
	-----> Preparing Python runtime (python-2.7.4)
	-----> Installing Distribute (0.6.36)
	-----> Installing Pip (1.3.1)
	-----> Noticed pylibmc. Bootstrapping libmemcached.
	-----> Installing dependencies using Pip (1.3.1)
	...
   	Successfully installed pylibmc django django-configurations django-secure django-cache-url dj-database-url django-braces django-crispy-forms django-floppyforms South django-model-utils Pillow django-allauth psycopg2 unicode-slugify django-autoslug django-avatar gunicorn django-storages gevent boto six python-openid requests-oauthlib requests django-appconf greenlet oauthlib
	Cleaning up...
	-----> Discovering process types
	       Procfile declares types -> web

	-----> Compiled slug size: 40.8MB
	-----> Launching... done, v10
	       http://{{cookiecutter.project_name}}.herokuapp.com deployed to Heroku

	To git@heroku.com:{{cookiecutter.project_name}}.git
	 * [new branch]      master -> master

Run the syncdb, migrate and collectstatic Django management commands::

	$ heroku run python {{cookiecutter.repo_name}}/manage.py syncdb --noinput --settings=config.settings
	$ heroku run python {{cookiecutter.repo_name}}/manage.py migrate --settings=config.settings
	$ heroku run python {{cookiecutter.repo_name}}/manage.py collectstatic --settings=config.settings

TODO: Explain how to serve static files with dj-static_.

.. _dj-static: https://github.com/kennethreitz/dj-static

Run this script: (TODO - automate this)

.. code-block:: python

    from django.contrib.sites.models import Site
    site = Site.objects.get()
    site.domain = "{{cookiecutter.domain_name}}"
    site.name = "{{cookiecutter.project_name}}"
    site.save()
