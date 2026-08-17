from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
{%- if cookiecutter.frontend_pipeline == 'Webpack' %}
from .base import WEBPACK_LOADER
{%- endif %}
from .base import env
{%- if cookiecutter.use_control_room == 'y' %}
from urllib.parse import urlparse
{%- endif %}

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="!!!SET DJANGO_SECRET_KEY!!!",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# EMAIL
# ------------------------------------------------------------------------------
{% if cookiecutter.mail_catcher == 'Mailpit' and cookiecutter.use_docker == 'y' -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
{%- elif cookiecutter.mail_catcher == 'Mailpit' and cookiecutter.use_docker == 'n' -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
{%- elif cookiecutter.mail_catcher == 'Mailtrap Local' and cookiecutter.use_docker == 'y' -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailtrap-local")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 3535
{%- elif cookiecutter.mail_catcher == 'Mailtrap Local' and cookiecutter.use_docker == 'n' -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 3535
{%- else -%}
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
{%- endif %}

{%- if cookiecutter.use_whitenoise == 'y' %}

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic", *INSTALLED_APPS]
{% endif %}

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # Disable profiling panel due to an issue with Python 3.12+:
        # https://github.com/jazzband/django-debug-toolbar/issues/1875
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
{% if cookiecutter.use_docker == 'y' -%}
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join([*ip.split(".")[:-1], "1"]) for ip in ips]
    {%- if cookiecutter.frontend_pipeline in ['Gulp', 'Webpack'] %}
    try:
        _, _, ips = socket.gethostbyname_ex("node")
        INTERNAL_IPS.extend(ips)
    except socket.gaierror:
        # The node container isn't started (yet?)
        pass
    {%- endif %}
    {%- if cookiecutter.windows == 'y' %}
    # RunServerPlus
    # ------------------------------------------------------------------------------
    # This is a custom setting for RunServerPlus to fix reloader issue in Windows docker environment
    # Werkzeug reloader type [auto, watchdog, or stat]
    RUNSERVERPLUS_POLLER_RELOADER_TYPE = 'stat'
    # If you have CPU and IO load issues, you can increase this poller interval e.g) 5
    RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 1
    {%- endif %}
{%- endif %}

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]
{% if cookiecutter.use_celery == 'y' -%}

{%- if cookiecutter.use_control_room == 'y' %}
# Django Control Room
# ------------------------------------------------------------------------------
DJ_CONTROL_ROOM_SETTINGS = {
    **DJ_CONTROL_ROOM_SETTINGS,
    "REGISTER_PANELS_IN_ADMIN": env.bool("CR_REGISTER_PANELS", default=True),
    "PANEL_ADMIN_REGISTRATION": {
        "dj_redis_panel": env.bool("CR_REGISTER_REDIS_PANEL", default=True),
        "dj_cache_panel": env.bool("CR_REGISTER_CACHE_PANEL", default=True),
        "dj_urls_panel": env.bool("CR_REGISTER_URLS_PANEL", default=True),
        "dj_signals_panel": env.bool("CR_REGISTER_SIGNALS_PANEL", default=True),
        "dj_celery_panel": env.bool("CR_REGISTER_CELERY_PANEL", default=True),
    },
}
REDIS_URL = env.str("REDIS_URL", default="redis://redis:6379/0") 
redis_url = urlparse(url=REDIS_URL) 
DJ_REDIS_PANEL_SETTINGS = {
     "ALLOW_KEY_DELETE": False, 
     "ALLOW_KEY_EDIT": False, 
     "ALLOW_TTL_UPDATE": False, 
     "CURSOR_PAGINATED_SCAN": False, 
     "CURSOR_PAGINATED_COLLECTIONS": False, 
     "socket_timeout": 5.0, 
     "socket_connect_timeout": 5.0, 
     "INSTANCES": { 
         "local_redis": { 
             "description": "Local Redis Instance", 
             "host": redis_url.hostname or "redis", 
             "port": redis_url.port or 6379, 
             "features": { 
                 "ALLOW_KEY_DELETE": True, 
                 "ALLOW_KEY_EDIT": True, 
                 "ALLOW_TTL_UPDATE": True, 
                 "CURSOR_PAGINATED_SCAN": True, 
                 "CURSOR_PAGINATED_COLLECTIONS": True, 
            }, 
        }, 
    }, 
}
{%- endif %}

# Celery
# ------------------------------------------------------------------------------
{% if cookiecutter.use_docker == 'n' -%}
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = True
{%- endif %}
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True

{%- endif %}
{%- if cookiecutter.frontend_pipeline == 'Webpack' %}
# django-webpack-loader
# ------------------------------------------------------------------------------
WEBPACK_LOADER["DEFAULT"]["CACHE"] = not DEBUG

{%- endif %}

# Adding local file storage for development
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Your stuff...
# ------------------------------------------------------------------------------
