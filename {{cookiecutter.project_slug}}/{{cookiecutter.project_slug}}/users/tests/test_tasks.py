import pytest
from celery.result import EagerResult

from {{ cookiecutter.project_slug }}.users.tasks import get_users_count
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """A basic test to execute the get_users_count Celery task."""
    settings.CELERY_TASK_ALWAYS_EAGER = True

    # Get all existing users in the DB
    current_users = get_users_count.delay()
    assert isinstance(current_users, EagerResult)

    # Create and add 3 more users to the DB.
    UserFactory.create_batch(3)

    # Get number of newly added users in the DB
    task_result = get_users_count.delay().result - current_users.result

    assert task_result == 3
