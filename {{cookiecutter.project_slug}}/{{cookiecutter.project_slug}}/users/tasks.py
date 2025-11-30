{% if cookiecutter.use_celery == 'y' -%}
from celery import shared_task
{%- elif cookiecutter.use_rq == 'y' -%}
import django_rq
{%- endif %}

from .models import User


{% if cookiecutter.use_celery == 'y' -%}
@shared_task()
{%- elif cookiecutter.use_rq == 'y' -%}
@django_rq.job
{%- endif %}
def get_users_count():
    """A pointless {% if cookiecutter.use_celery == 'y' %}Celery{% elif cookiecutter.use_rq == 'y' %}RQ{% endif %} task to demonstrate usage."""
    return User.objects.count()
