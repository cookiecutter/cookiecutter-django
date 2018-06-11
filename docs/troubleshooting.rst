Troubleshooting
=====================================

This page contains some advice about errors and problems commonly encountered during the development of Cookiecutter Django applications.

#. ``project_slug`` must be a valid Python module name or you will have issues on imports.

#. ``jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'now'.``: please upgrade your cookiecutter version to >= 1.4 (see `#528`_)

#. Internal server error on user registration: make sure you have configured the mail backend (e.g. Mailgun) by adding the API key and sender domain

.. _#528: https://github.com/pydanny/cookiecutter-django/issues/528#issuecomment-212650373
