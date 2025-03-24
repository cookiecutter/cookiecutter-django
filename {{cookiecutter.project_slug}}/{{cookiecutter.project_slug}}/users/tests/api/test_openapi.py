from http import HTTPStatus

import pytest
from django.conf import settings
from django.urls import NoReverseMatch
from django.urls import reverse


@pytest.mark.skipif(not settings.DEBUG, reason="Swagger is implemented only in debug mode")
def test_swagger_accessible_by_admin(admin_client):
    url = reverse("api-docs")
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skipif(not settings.DEBUG, reason="Swagger is implemented only in debug mode")
@pytest.mark.django_db
def test_swagger_ui_not_accessible(client):
    url = reverse("api-docs")
    response = client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.skipif(not settings.DEBUG, reason="Swagger is implemented only in debug mode")
def test_api_schema_generated_successfully(admin_client):
    url = reverse("api-schema")
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skipif(settings.DEBUG, reason="Swagger is implemented only in debug mode")
def test_swagger_not_accessible():
    assert not settings.DEBUG, "Swagger is implemented only in debug mode"

    with pytest.raises(NoReverseMatch):
        reverse("api-docs")
