from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_django.fixtures import Settings

    from {{ cookiecutter.project_slug }}.users.models import User


@pytest.fixture(autouse=True)
def _media_storage(settings: Settings, tmp_path: Path) -> None:
    settings.MEDIA_ROOT = str(tmp_path)


@pytest.fixture
def user(db: None) -> User:
    return UserFactory.create()
