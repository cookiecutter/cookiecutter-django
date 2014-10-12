# -*- coding: utf-8 -*-
{% if cookiecutter.use_celery == "y" %}
from __future__ import absolute_import
from {{cookiecutter.repo_name}}.celery import app as celery_app
{% endif %}
__version__ = '{{ cookiecutter.version }}'
__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace('-', '.', 1).split('.')])
