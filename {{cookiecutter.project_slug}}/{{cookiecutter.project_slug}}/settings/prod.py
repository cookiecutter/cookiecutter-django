from .base import *  # noqa
from .base import env  # noqa
{% if cookiecutter.use_sentry == 'y' -%}
import logging

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
{% if cookiecutter.use_celery == 'y' -%}
from sentry_sdk.integrations.celery import CeleryIntegration
{% endif %}{% endif %}

DEBUG = False  # Forcible override to turn DEBUG off in production

# TEMPLATES
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# LOGGING
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        {%- if cookiecutter.use_sentry == 'y' %}
        "sentry_sdk": {  # Errors logged by Sentry's SDK itself
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        {%- endif %}
    },
}

{%- if cookiecutter.use_sentry == 'y' %}
# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
{%- if cookiecutter.use_celery == 'y' %}
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[sentry_logging, DjangoIntegration(), CeleryIntegration()],
)
{%- else %}
sentry_sdk.init(dsn=SENTRY_DSN, integrations=[sentry_logging, DjangoIntegration()])
{%- endif %}
{%- endif %}
