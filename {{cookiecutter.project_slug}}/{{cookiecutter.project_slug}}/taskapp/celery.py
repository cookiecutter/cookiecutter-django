{% if cookiecutter.use_celery == 'y' %}
import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('{{cookiecutter.project_slug}}')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


class CeleryAppConfig(AppConfig):
    name = '{{cookiecutter.project_slug}}.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        {% if cookiecutter.use_sentry == 'y' -%}
        if hasattr(settings, "SENTRY_DSN"):
            # Celery signal registration
            {% if cookiecutter.use_pycharm == 'y' -%}
	        # Since Sentry is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            # @formatter:off
            {%- endif %}
            import sentry_sdk
            from sentry_sdk.integrations.celery import CeleryIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration
            {% if cookiecutter.use_pycharm == 'y' -%}
            # @formatter:on
            {%- endif %}
            sentry_logging = LoggingIntegration(
                level=settings.SENTRY_LOGLEVEL,  # Capture info and above as breadcrumbs
                event_level=None,  # Send no events from log messages
            )
            sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[sentry_logging, CeleryIntegration()])
        {%- endif %}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # pragma: no cover
{% else %}
# Use this as a starting point for your project with celery.
# If you are not using celery, you can remove this app
{% endif -%}
