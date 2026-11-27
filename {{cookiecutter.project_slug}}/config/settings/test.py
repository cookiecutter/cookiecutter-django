"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
{%- if cookiecutter.use_mockatoo == 'y' %}
from .base import INSTALLED_APPS
{%- endif %}
from .base import TEMPLATES
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="!!!SET DJANGO_SECRET_KEY!!!",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver/"

{%- if cookiecutter.frontend_pipeline == 'Webpack' %}
# django-webpack-loader
# ------------------------------------------------------------------------------
WEBPACK_LOADER["DEFAULT"]["LOADER_CLASS"] = "webpack_loader.loaders.FakeWebpackLoader"  # noqa: F405

{%- endif %}
{%- if cookiecutter.use_mockatoo == 'y' %}

# Mockatoo
# ------------------------------------------------------------------------------
# GitHub sign-in through Mockatoo, a mock OAuth provider, so no OAuth app is needed.
# https://mockatoo.globalunderdog.com/docs/django
INSTALLED_APPS += ["allauth.socialaccount.providers.github"]
# https://docs.allauth.org/en/latest/socialaccount/providers/github.html
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "GITHUB_URL": "https://app.mockatoo.globalunderdog.com/github",
        "SCOPE": ["user:email"],
        "APPS": [{"client_id": "mockatoo", "secret": "mockatoo-secret"}],
    },
}
{%- endif %}
# Your stuff...
# ------------------------------------------------------------------------------
