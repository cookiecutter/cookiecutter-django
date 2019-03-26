Troubleshooting
=====================================

This page contains some advice about errors and problems commonly encountered during the development of Cookiecutter Django applications.

#. ``project_slug`` must be a valid Python module name or you will have issues on imports.

#. ``jinja2.exceptions.TemplateSyntaxError: Encountered unknown tag 'now'.``: please upgrade your cookiecutter version to >= 1.4 (see `#528`_)

#. Internal server error on user registration: make sure you have configured the mail backend (e.g. Mailgun) by adding the API key and sender domain

#. New apps not getting created in project root: This is the expected behavior, because cookiecutter-django does not change the way that django startapp works, you'll have to fix this manually (see `#1725`_)

#. .. include:: mailgun.rst

.. _#528: https://github.com/pydanny/cookiecutter-django/issues/528#issuecomment-212650373
.. _#1725: https://github.com/pydanny/cookiecutter-django/issues/1725#issuecomment-407493176
