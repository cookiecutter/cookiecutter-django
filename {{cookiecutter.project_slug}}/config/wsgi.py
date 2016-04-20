"""
WSGI config for {{ cookiecutter.project_name }} project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

{% if cookiecutter.use_newrelic == 'y' -%}
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    import newrelic.agent
    newrelic.agent.initialize()
{%- endif %}
from django.core.wsgi import get_wsgi_application
{% if cookiecutter.use_whitenoise == 'y' -%}
from whitenoise.django import DjangoWhiteNoise
{%- endif %}
{% if cookiecutter.use_sentry == 'y' -%}
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
{%- endif %}

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

{% if cookiecutter.use_whitenoise == 'y' -%}
# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.org/
application = DjangoWhiteNoise(application)
{%- endif %}
{% if cookiecutter.use_sentry == 'y' -%}
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    application = Sentry(application)
{%- endif %}
{% if cookiecutter.use_newrelic == 'y' -%}
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    application = newrelic.agent.WSGIApplicationWrapper(application)
{%- endif %}
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
