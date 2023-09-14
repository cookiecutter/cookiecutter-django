{% if cookiecutter.use_sentry == 'y' -%}
import logging

import sentry_sdk

{%- if cookiecutter.use_celery == 'y' %}
from sentry_sdk.integrations.celery import CeleryIntegration

{%- endif %}
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

{% endif -%}
from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["{{ cookiecutter.domain_name }}"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa: F405

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

{% if cookiecutter.cloud_provider != 'None' -%}
# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa: F405
{%- endif -%}
{% if cookiecutter.cloud_provider == 'AWS' %}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_MAX_MEMORY_SIZE = env.int(
    "DJANGO_AWS_S3_MAX_MEMORY_SIZE",
    default=100_000_000,  # 100MB
)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
AWS_S3_CUSTOM_DOMAIN = env("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
{% elif cookiecutter.cloud_provider == 'GCP' %}
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"
{% elif cookiecutter.cloud_provider == 'Azure' %}
AZURE_ACCOUNT_KEY = env("DJANGO_AZURE_ACCOUNT_KEY")
AZURE_ACCOUNT_NAME = env("DJANGO_AZURE_ACCOUNT_NAME")
AZURE_CONTAINER = env("DJANGO_AZURE_CONTAINER_NAME")
{% endif -%}

{% if cookiecutter.cloud_provider != 'None' or cookiecutter.use_whitenoise == 'y' -%}
# STATIC
# ------------------------
{% endif -%}
{% if cookiecutter.use_whitenoise == 'y' -%}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
{% elif cookiecutter.cloud_provider == 'AWS' -%}
STATICFILES_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.StaticS3Storage"
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATIC_URL = f"https://{aws_s3_domain}/static/"
{% elif cookiecutter.cloud_provider == 'GCP' -%}
STATICFILES_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.StaticGoogleCloudStorage"
COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
{% elif cookiecutter.cloud_provider == 'Azure' -%}
STATICFILES_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.StaticAzureStorage"
STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/static/"
{% endif -%}

# MEDIA
# ------------------------------------------------------------------------------
{%- if cookiecutter.cloud_provider == 'AWS' %}
DEFAULT_FILE_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.MediaS3Storage"
MEDIA_URL = f"https://{aws_s3_domain}/media/"
{%- elif cookiecutter.cloud_provider == 'GCP' %}
DEFAULT_FILE_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.MediaGoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
{%- elif cookiecutter.cloud_provider == 'Azure' %}
DEFAULT_FILE_STORAGE = "{{cookiecutter.project_slug}}.utils.storages.MediaAzureStorage"
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/media/"
{%- endif %}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="{{cookiecutter.project_name}} <noreply@{{cookiecutter.domain_name}}>",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[{{cookiecutter.project_name}}] ",
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")

# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]  # noqa: F405
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
{%- if cookiecutter.mail_service == 'Mailgun' %}
# https://anymail.readthedocs.io/en/stable/esps/mailgun/
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
    "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
}
{%- elif cookiecutter.mail_service == 'Amazon SES' %}
# https://anymail.readthedocs.io/en/stable/esps/amazon_ses/
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
ANYMAIL = {}
{%- elif cookiecutter.mail_service == 'Mailjet' %}
# https://anymail.readthedocs.io/en/stable/esps/mailjet/
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
ANYMAIL = {
    "MAILJET_API_KEY": env("MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY": env("MAILJET_SECRET_KEY"),
}
{%- elif cookiecutter.mail_service == 'Mandrill' %}
# https://anymail.readthedocs.io/en/stable/esps/mandrill/
EMAIL_BACKEND = "anymail.backends.mandrill.EmailBackend"
ANYMAIL = {
    "MANDRILL_API_KEY": env("MANDRILL_API_KEY"),
    "MANDRILL_API_URL": env("MANDRILL_API_URL", default="https://mandrillapp.com/api/1.0"),
}
{%- elif cookiecutter.mail_service == 'Postmark' %}
# https://anymail.readthedocs.io/en/stable/esps/postmark/
EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"
ANYMAIL = {
    "POSTMARK_SERVER_TOKEN": env("POSTMARK_SERVER_TOKEN"),
    "POSTMARK_API_URL": env("POSTMARK_API_URL", default="https://api.postmarkapp.com/"),
}
{%- elif cookiecutter.mail_service == 'Sendgrid' %}
# https://anymail.readthedocs.io/en/stable/esps/sendgrid/
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": env("SENDGRID_API_KEY"),
    "SENDGRID_API_URL": env("SENDGRID_API_URL", default="https://api.sendgrid.com/v3/"),
}
{%- elif cookiecutter.mail_service == 'SendinBlue' %}
# https://anymail.readthedocs.io/en/stable/esps/sendinblue/
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
ANYMAIL = {
    "SENDINBLUE_API_KEY": env("SENDINBLUE_API_KEY"),
    "SENDINBLUE_API_URL": env("SENDINBLUE_API_URL", default="https://api.sendinblue.com/v3/"),
}
{%- elif cookiecutter.mail_service == 'SparkPost' %}
# https://anymail.readthedocs.io/en/stable/esps/sparkpost/
EMAIL_BACKEND = "anymail.backends.sparkpost.EmailBackend"
ANYMAIL = {
    "SPARKPOST_API_KEY": env("SPARKPOST_API_KEY"),
    "SPARKPOST_API_URL": env("SPARKPOST_API_URL", default="https://api.sparkpost.com/api/v1"),
}
{%- elif cookiecutter.mail_service == 'Other SMTP' %}
# https://anymail.readthedocs.io/en/stable/esps
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}
{%- endif %}

{% if cookiecutter.frontend_pipeline == 'Django Compressor' -%}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
{%- if cookiecutter.cloud_provider == 'None' %}
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
{%- elif cookiecutter.cloud_provider in ('AWS', 'GCP', 'Azure') and cookiecutter.use_whitenoise == 'n' %}
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = STATICFILES_STORAGE
{%- endif %}
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL{% if cookiecutter.use_whitenoise == 'y' or cookiecutter.cloud_provider == 'None' %}  # noqa: F405{% endif %}
{%- if cookiecutter.use_whitenoise == 'y' %}
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True  # Offline compression is required when using Whitenoise
{%- endif %}
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}
{% endif %}
{%- if cookiecutter.use_whitenoise == 'n' -%}
# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS  # noqa: F405
{% endif %}
# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
{% if cookiecutter.use_sentry == 'n' -%}
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}
{% else %}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
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
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

{%- if cookiecutter.use_celery == 'y' %}
integrations = [
    sentry_logging,
    DjangoIntegration(),
    CeleryIntegration(),
    RedisIntegration(),
]
{% else %}
integrations = [sentry_logging, DjangoIntegration(), RedisIntegration()]
{% endif -%}

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="production"),
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
)
{% endif %}
{% if cookiecutter.use_drf == "y" -%}

# django-rest-framework
# -------------------------------------------------------------------------------
# Tools that generate code samples can use SERVERS to point to the correct domain
SPECTACULAR_SETTINGS["SERVERS"] = [  # noqa: F405
    {"url": "https://{{ cookiecutter.domain_name }}", "description": "Production server"},
]

{%- endif %}
# Your stuff...
# ------------------------------------------------------------------------------
