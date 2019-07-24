"""
Base settings to build other settings files upon.
"""
import environ

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # ({{ cookiecutter.project_slug }}/config/settings/base.py - 3 = {{ cookiecutter.project_slug }}/)
APPS_DIR = ROOT_DIR.path("{{ cookiecutter.project_slug }}")

env = environ.Env()

# OS environment variables take precedence over variables from .env
env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
SITE_ID = 1
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[".{{ cookiecutter.domain_name }}"])


# DATABASES
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)


# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"
WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"


# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
{%- if cookiecutter.use_celery == 'y' %}
    "django_celery_beat",
{%- endif %}
{%- if cookiecutter.use_compressor == 'y' %}
    "compressor",
{%- endif %}
{%- if cookiecutter.cloud_provider != 'None' %}
    "storages",
{%- endif %}
]

LOCAL_APPS = [
    "{{ cookiecutter.project_slug }}.users.apps.UsersConfig",
    # Your stuff: custom apps go here
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# CACHES
# https://docs.djangoproject.com/en/2.2/ref/settings/#caches
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}


# SECURITY
# ------------------------------------------------------------------------------
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECRET_KEY = env("DJANGO_SECRET_KEY")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"


# SESSIONS
# https://docs.djangoproject.com/en/2.2/ref/settings/#sessions
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# MIGRATIONS
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "{{ cookiecutter.project_slug }}.contrib.sites.migrations"}


# AUTHENTICATION
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"

# use named URL patterns instead of hardcoded paths
LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_URL = "account_login"
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
{%- if cookiecutter.use_whitenoise == 'y' %}
    "whitenoise.middleware.WhiteNoiseMiddleware",
{%- endif %}
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Globalization (i18n/l10n)
# https://docs.djangoproject.com/en/2.2/ref/settings/#globalization-i18n-l10n
# ------------------------------------------------------------------------------
TIME_ZONE = "{{ cookiecutter.timezone }}"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [ROOT_DIR.path("locale")]

{%- if cookiecutter.cloud_provider != 'None' %}


# STORAGES
# https://django-storages.readthedocs.io/en/latest/#installation
# ------------------------------------------------------------------------------
{% if cookiecutter.cloud_provider == 'AWS' %}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
{% elif cookiecutter.cloud_provider == 'GCP' %}
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"
{% elif cookiecutter.cloud_provider == 'Azure' %}
# https://django-storages.readthedocs.io/en/latest/backends/azure.html#install
AZURE_ACCOUNT_NAME = env("DJANGO_AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = env("DJANGO_AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = env("DJANGO_AZURE_CONTAINER")
AZURE_URL_EXPIRATION_SECS = 60 * 60 * 24 * 7
{% endif -%}


# STATIC
# https://docs.djangoproject.com/en/2.2/ref/settings/#static-files
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
{%- if cookiecutter.use_compressor == 'y' %}
    "compressor.finders.CompressorFinder",
{%- endif %}
]
{%- if cookiecutter.cloud_provider == 'AWS' %}
STATICFILES_STORAGE = "{{ cookiecutter.project_slug }}.storage.StaticRootS3Boto3Storage"
STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/"
{% elif cookiecutter.cloud_provider == 'GCP' %}
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
{% elif cookiecutter.cloud_provider == 'Azure' %}
STATICFILES_STORAGE = "{{ cookiecutter.project_slug }}.storage.PublicAzureStorage"
{% elif cookiecutter.use_whitenoise == 'y' %}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
{% else %}
STATIC_URL = "/static/"
{%- endif %}
{%- if cookiecutter.use_compressor == 'y' %}
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL
{% endif %}

{%- endif %}

# FILE UPLOADS
# https://docs.djangoproject.com/en/2.2/ref/settings/#file-uploads
# ------------------------------------------------------------------------------
{%- if cookiecutter.cloud_provider == 'AWS' %}
DEFAULT_FILE_STORAGE = "{{ cookiecutter.project_slug }}.storage.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"
{% elif cookiecutter.cloud_provider == 'GCP' %}
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
MEDIA_ROOT = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
{% elif cookiecutter.cloud_provider == 'Azure' %}
DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
{% else %}
MEDIA_ROOT = str(ROOT_DIR("media"))
MEDIA_URL = "/media/"
{%- endif %}

# TEMPLATES
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)


# EMAIL
# https://docs.djangoproject.com/en/2.2/ref/settings/#email
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_TIMEOUT = 5

EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env.int("EMAIL_PORT", 25)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[{{cookiecutter.project_name}}]"
)
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="{{cookiecutter.project_name}} <noreply@{{cookiecutter.domain_name}}>"
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
ADMINS = [("""{{cookiecutter.author_name}}""", "{{cookiecutter.email}}")]
MANAGERS = ADMINS

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
    },
}
{%- if cookiecutter.use_celery == 'y' %}


# Celery
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
# ------------------------------------------------------------------------------
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
{%- endif %}

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "{{cookiecutter.project_slug}}.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "{{cookiecutter.project_slug}}.users.adapters.SocialAccountAdapter"


# Your stuff...
# ------------------------------------------------------------------------------
