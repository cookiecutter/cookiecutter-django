from http import HTTPStatus

import pytest
from django.urls import reverse


def test_api_docs_accessible_by_admin(admin_client):
    {%- if cookiecutter.rest_api == 'DRF' %}
    url = reverse("api-docs")
    {%- elif cookiecutter.rest_api == 'Django Ninja' %}
    url = reverse("api:openapi-view")
    {%- else %}
    pytest.skip("No REST API framework selected")
    {%- endif %}
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_api_docs_not_accessible_by_anonymous_users(client):
    {%- if cookiecutter.rest_api == 'DRF' %}
    url = reverse("api-docs")
    response = client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN
    {%- elif cookiecutter.rest_api == 'Django Ninja' %}
    url = reverse("api:openapi-view")
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/admin/login/?next=/api/docs"
    {%- else %}
    pytest.skip("No REST API framework selected")
    {%- endif %}


def test_api_schema_generated_successfully(admin_client):
    {%- if cookiecutter.rest_api == 'DRF' %}
    url = reverse("api-schema")
    {%- elif cookiecutter.rest_api == 'Django Ninja' %}
    url = reverse("api:openapi-json")
    {%- else %}
    pytest.skip("No REST API framework selected")
    {%- endif %}
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
