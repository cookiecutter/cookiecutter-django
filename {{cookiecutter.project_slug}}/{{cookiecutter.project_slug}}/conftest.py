import pytest

from {{ cookiecutter.project_slug }}.users.models import User
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()
