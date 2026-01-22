from ninja.testing import TestClient
from {{ cookiecutter.project_slug }}.users.api.controllers import router
from {{ cookiecutter.project_slug }}.users.models import User
import pytest

@pytest.fixture
def user():
    return User.objects.create(username="testuser", password="password")

@pytest.mark.django_db
def test_get_users(user):
    client = TestClient(router)
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "testuser"
