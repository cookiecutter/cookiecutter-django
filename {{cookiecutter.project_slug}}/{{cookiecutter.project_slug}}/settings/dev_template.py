from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
{% if cookiecutter.use_mailhog == 'y' -%}
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
{%- else -%}
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = "localhost"
{%- endif %}
EMAIL_PORT = 1025

# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env.bool("USE_DOCKER", False) == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

# django-extensions
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]  # noqa F405
{% if cookiecutter.use_celery == 'y' -%}

# Celery
# ------------------------------------------------------------------------------
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

{%- endif %}
# Your stuff...
# ------------------------------------------------------------------------------
