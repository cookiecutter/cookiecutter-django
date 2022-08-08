from django.urls import resolve, reverse

from {{ cookiecutter.project_slug }}.users.models import User


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.uuid})
        == f"/users/{user.uuid}/"
    )
    assert resolve(f"/users/{user.uuid}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"
