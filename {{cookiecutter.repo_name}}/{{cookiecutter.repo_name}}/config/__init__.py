# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from .local import Local  # noqa
from .production import Production  # noqa


try:
    from django.conf import settings
    from django.core.checks import register, Error
    @register(settings)
    def dj_database_url_check(app_configs=None, **kwargs):
        errors = []
        password = settings.DATABASES['default'].get('PASSWORD')
        config = os.environ['DJANGO_CONFIGURATION'].lower()
        if password == 'blank' and config == 'production':
            errors.append(Error('Change the database password for production.'))
        return errors
except ImportError:
    pass
