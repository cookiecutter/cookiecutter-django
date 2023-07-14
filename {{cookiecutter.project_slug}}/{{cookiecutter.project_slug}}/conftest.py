import pytest

from {{ cookiecutter.project_slug }}.users.models import User
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(autouse=True)
def media_url(settings):
    settings.MEDIA_URL = 'http://testserver'


@pytest.fixture
def user(db) -> User:
    return UserFactory()
