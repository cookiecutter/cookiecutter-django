"""
Local settings

- Run in Debug mode
{% if cookiecutter.use_mailhog == 'y' and cookiecutter.use_docker == 'y' %}
- Use mailhog for emails
{% elif cookiecutter.use_mailhog == 'y' and cookiecutter.use_docker == 'n' %}
- Use mailhog for emails
{% else %}
- Use console backend for emails
{% endif %}
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='CHANGEME!!!')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025
{% if cookiecutter.use_mailhog == 'y' and cookiecutter.use_docker == 'y' %}
EMAIL_HOST = env('EMAIL_HOST', default='mailhog')
{% elif cookiecutter.use_mailhog == 'y' and cookiecutter.use_docker == 'n' %}
EMAIL_HOST = 'localhost'
{% else %}
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')
{% endif %}

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
{% if cookiecutter.use_docker == 'y' %}
{# [cookiecutter-django] This is a workaround to flake8 "imported but unused" errors #}
import socket
import os
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']
{% endif %}
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
{% if cookiecutter.use_celery == 'y' %}
########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY
{% endif %}
# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
