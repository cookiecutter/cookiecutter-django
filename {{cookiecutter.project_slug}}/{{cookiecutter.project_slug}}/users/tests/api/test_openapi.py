{%- if cookiecutter.rest_api != 'None' %}
from http import HTTPStatus

import pytest
from django.urls import reverse


def test_api_docs_accessible_by_admin(admin_client):
    {%- if cookiecutter.rest_api == 'DRF' %}
    url = reverse("api-docs")
    {%- elif cookiecutter.rest_api == 'Django Ninja' %}
    url = reverse("api:openapi-view")
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
    {%- endif %}


def test_api_schema_generated_successfully(admin_client):
    {%- if cookiecutter.rest_api == 'DRF' %}
    url = reverse("api-schema")
    {%- elif cookiecutter.rest_api == 'Django Ninja' %}
    url = reverse("api:openapi-json")
    {%- endif %}
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK
{%- else %}
# No REST API framework was selected (rest_api = 'None').
# These tests are not applicable to this configuration.
# When hooks are enabled, the post-generation hook removes this directory entirely.
{%- endif %}
