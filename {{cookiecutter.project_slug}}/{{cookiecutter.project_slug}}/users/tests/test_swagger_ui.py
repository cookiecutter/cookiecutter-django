import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_swagger_accessible_by_admin(admin_client):
    url = reverse("api-docs")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_swagger_ui_not_accessible_by_normal_user(client):
    url = reverse("api-docs")
    response = client.get(url)
    assert response.status_code == 403
