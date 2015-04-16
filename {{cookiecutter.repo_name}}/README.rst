{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}


LICENSE: BSD

Settings
------------

{{cookiecutter.project_name}} relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, see the table maps the '{{cookiecutter.project_name}}' environment variables to their Django setting: https://{{ cookiecutter.repo_name }}.readthedocs.org/en/latest/install.html#Settings

Getting up and running
----------------------

Just follow the steps described in https://{{ cookiecutter.repo_name }}.readthedocs.org/en/latest/install.html and you'll get yourself an up and running local development environment.

Deployment
------------

The instructions for deployment can be found at https://{{ cookiecutter.repo_name }}.readthedocs.org/en/latest/deploy.html
