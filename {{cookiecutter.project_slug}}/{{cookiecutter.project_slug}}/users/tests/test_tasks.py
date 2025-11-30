import pytest
{% if cookiecutter.use_celery == 'y' -%}
from celery.result import EagerResult
{%- elif cookiecutter.use_rq == 'y' -%}
import django_rq
{%- endif %}

from {{ cookiecutter.project_slug }}.users.tasks import get_users_count
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """A basic test to execute the get_users_count {% if cookiecutter.use_celery == 'y' %}Celery{% elif cookiecutter.use_rq == 'y' %}RQ{% endif %} task."""
    batch_size = 3
    UserFactory.create_batch(batch_size)
{% if cookiecutter.use_celery == 'y' -%}
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = get_users_count.delay()
    assert isinstance(task_result, EagerResult)
    assert task_result.result == batch_size
{%- elif cookiecutter.use_rq == 'y' -%}
    queue = django_rq.get_queue("default", is_async=False)
    job = queue.enqueue(get_users_count)
    assert job.result == batch_size
{%- endif %}
