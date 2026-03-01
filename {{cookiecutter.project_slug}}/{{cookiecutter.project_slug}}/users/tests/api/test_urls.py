from django.urls import resolve
from django.urls import reverse

from {{ cookiecutter.project_slug }}.users.models import User
{%- if cookiecutter.rest_api == 'DRF' %}


def test_user_detail(user: User):
    {%- if cookiecutter.username_type == "email" %}
    assert (
        reverse("api:user-detail", kwargs={"pk": user.pk}) == f"/api/users/{user.pk}/"
    )
    assert resolve(f"/api/users/{user.pk}/").view_name == "api:user-detail"
    {%- else %}
    assert (
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/api/users/{user.username}/"
    )
    assert resolve(f"/api/users/{user.username}/").view_name == "api:user-detail"
    {%- endif %}


def test_user_list():
    assert reverse("api:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:user-list"


def test_user_me():
    assert reverse("api:user-me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:user-me"
{%- elif cookiecutter.rest_api == 'Django Ninja' %}


def test_user_detail(user: User):
    {%- if cookiecutter.username_type == "email" %}
    assert (
        reverse("api:retrieve_user", kwargs={"pk": user.pk}) == f"/api/users/{user.pk}/"
    )
    assert resolve(f"/api/users/{user.pk}/").view_name == "api:retrieve_user"
    {%- else %}
    assert (
        reverse("api:retrieve_user", kwargs={"username": user.username})
        == f"/api/users/{user.username}/"
    )
    assert resolve(f"/api/users/{user.username}/").view_name == "api:retrieve_user"
    {%- endif %}


def test_user_list():
    assert reverse("api:list_users") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:list_users"


def test_current_user():
    assert reverse("api:retrieve_current_user") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:retrieve_current_user"


def test_update_user():
    {%- if cookiecutter.username_type == "email" %}
    assert reverse("api:update_user", kwargs={"pk": 123}) == "/api/users/123/"
    assert resolve("/api/users/123/").view_name == "api:retrieve_user"
    {%- else %}
    assert reverse("api:update_user", kwargs={"username": "johndoe"}) == "/api/users/johndoe/"
    assert resolve("/api/users/johndoe/").view_name == "api:retrieve_user"
    {%- endif %}
{%- endif %}
