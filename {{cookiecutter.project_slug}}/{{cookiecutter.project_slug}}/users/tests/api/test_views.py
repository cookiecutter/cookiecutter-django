{% if cookiecutter.rest_api == 'DRF' -%}
import pytest
from rest_framework.test import APIRequestFactory

from {{ cookiecutter.project_slug }}.users.api.views import UserViewSet
from {{ cookiecutter.project_slug }}.users.models import User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore[call-arg, arg-type, misc]

        assert response.data == {
            {%- if cookiecutter.username_type == "email" %}
            "url": f"http://testserver/api/users/{user.pk}/",
            {%- else %}
            "username": user.username,
            "url": f"http://testserver/api/users/{user.username}/",
            {%- endif %}
            "name": user.name,
        }
{%- elif cookiecutter.rest_api == 'Django Ninja' -%}
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from {{ cookiecutter.project_slug }}.users.models import User
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return UserFactory()


def test_list_users_as_anonymous_user(client: Client):
    response = client.get(reverse("api:list_users"))

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_list_users_as_authenticated_user(client: Client, user: User):
    client.force_login(user)
    # Another user, excluded from the response
    UserFactory()

    response = client.get(reverse("api:list_users"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "email": user.email,
            "name": user.name,
            {%- if cookiecutter.username_type == "email" %}
            "url": f"/api/users/{user.pk}/",
            {%- else %}
            "url": f"/api/users/{user.username}/",
            "username": user.username,
            {%- endif %}
        },
    ]
{%- if cookiecutter.username_type == "email" %}


@pytest.mark.parametrize("user_pk", [None, "me"])
def test_retrieve_user(client: Client, user: User, user_pk: str | None):
    client.force_login(user)
    user_pk = user_pk or user.pk

    response = client.get(
        reverse("api:retrieve_user", kwargs={"pk": user_pk}),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.pk}/",
    }
{%- else %}


@pytest.mark.parametrize("username", [None, "me"])
def test_retrieve_user(client: Client, user: User, username: str | None):
    client.force_login(user)
    username = username or user.username

    response = client.get(
        reverse("api:retrieve_user", kwargs={"username": username}),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }
{%- endif %}


def test_retrieve_another_user(client: Client, user: User):
    client.force_login(user)
    user_2 = UserFactory()

    response = client.get(
        {%- if cookiecutter.username_type == "email" %}
        reverse("api:retrieve_user", kwargs={"pk": user_2.pk}),
        {%- else %}
        reverse("api:retrieve_user", kwargs={"username": user_2.username}),
        {%- endif %}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Not Found"}

{%- if cookiecutter.username_type == "email" %}


def test_update_user(client: Client):
    user = UserFactory(name="Old")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_user", kwargs={"pk": user.pk}),
        data='{"name": "New Name"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        "email": user.email,
        "name": "New Name",
        "url": f"/api/users/{user.pk}/",
    }
{%- else %}


def test_update_user(client: Client):
    user = UserFactory(name="Old", username="old")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_user", kwargs={"username": "old"}),
        data='{"name": "New Name", "username": "old"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        "email": user.email,
        "name": "New Name",
        "url": "/api/users/old/",
        "username": "old",
    }
{%- endif %}
{%- endif %}
