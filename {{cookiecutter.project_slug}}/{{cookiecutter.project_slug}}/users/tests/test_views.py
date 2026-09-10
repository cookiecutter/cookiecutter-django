from __future__ import annotations

import re
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_htmx.middleware import HtmxDetails

from {{ cookiecutter.project_slug }}.users.forms import UserAdminChangeForm
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory
from {{ cookiecutter.project_slug }}.users.views import UserRedirectView
from {{ cookiecutter.project_slug }}.users.views import UserUpdateView
from {{ cookiecutter.project_slug }}.users.views import user_detail_view

if TYPE_CHECKING:
    from django.test import RequestFactory

    from {{ cookiecutter.project_slug }}.users.models import User

pytestmark = pytest.mark.django_db

HTMX_HEADERS = {"HX-Request": "true"}


def template_names(response) -> list[str]:
    return [template.name for template in response.templates if template.name]


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.setup(request)

        {%- if cookiecutter.username_type == "email" %}
        assert view.get_success_url() == f"/users/{user.pk}/"
        {%- else %}
        assert view.get_success_url() == f"/users/{user.username}/"
        {%- endif %}

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.setup(request)

        assert view.get_object() == user

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.setup(request)

        # Initialize the form
        form = UserAdminChangeForm()
        form.cleaned_data = {}
        form.instance = user
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [_("Information successfully updated")]

    def test_get_full_page(self, user: User, client: Client):
        client.force_login(user)

        response = client.get(reverse("users:update"))

        assert response.status_code == HTTPStatus.OK
        assert template_names(response)[0] == "users/user_form.html"
        assert b"<html" in response.content
        assert b'id="user-profile"' in response.content

    def test_get_htmx_partial(self, user: User, client: Client):
        client.force_login(user)

        response = client.get(reverse("users:update"), headers=HTMX_HEADERS)

        assert response.status_code == HTTPStatus.OK
        assert template_names(response)[0] == "users/partials/user_form.html"
        assert "base.html" not in template_names(response)
        assert b"<html" not in response.content
        assert b'id="user-profile"' in response.content
        assert "HX-Request" in response["Vary"]

    def test_post_without_csrf_token_is_forbidden(self, user: User):
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        client.get(reverse("users:update"))  # sets the CSRF cookie

        response = client.post(
            reverse("users:update"),
            {"name": "New Name"},
            headers=HTMX_HEADERS,
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        user.refresh_from_db()
        assert user.name != "New Name"

    def test_post_with_csrf_header(self, user: User):
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        page = client.get(reverse("users:update"))
        # The token htmx sends comes from the hx-headers attribute on <body>
        match = re.search(r'"X-CSRFToken": "([^"]+)"', page.content.decode())
        assert match

        response = client.post(
            reverse("users:update"),
            {"name": "New Name"},
            headers={**HTMX_HEADERS, "X-CSRFToken": match.group(1)},
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response["Location"] == user.get_absolute_url()
        user.refresh_from_db()
        assert user.name == "New Name"

    def test_htmx_post_redirects_to_detail_partial(self, user: User, client: Client):
        client.force_login(user)

        response = client.post(
            reverse("users:update"),
            {"name": "New Name"},
            headers=HTMX_HEADERS,
            follow=True,
        )

        assert response.redirect_chain == [(user.get_absolute_url(), HTTPStatus.FOUND)]
        assert template_names(response)[0] == "users/partials/user_detail.html"
        assert b'id="messages" hx-swap-oob="true"' in response.content
        assert str(_("Information successfully updated")).encode() in response.content


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.setup(request)

        {%- if cookiecutter.username_type == "email" %}
        assert view.get_redirect_url() == f"/users/{user.pk}/"
        {%- else %}
        assert view.get_redirect_url() == f"/users/{user.username}/"
        {%- endif %}


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory.create()
        request.htmx = HtmxDetails(request)  # type: ignore[attr-defined]

        {%- if cookiecutter.username_type == "email" %}
        response = user_detail_view(request, pk=user.pk)
        {%- else %}
        response = user_detail_view(request, username=user.username)
        {%- endif %}

        assert response.status_code == HTTPStatus.OK

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()
        request.htmx = HtmxDetails(request)  # type: ignore[attr-defined]

        {%- if cookiecutter.username_type == "email" %}
        response = user_detail_view(request, pk=user.pk)
        {%- else %}
        response = user_detail_view(request, username=user.username)
        {%- endif %}
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_full_page(self, user: User, client: Client):
        client.force_login(user)

        response = client.get(user.get_absolute_url())

        assert response.status_code == HTTPStatus.OK
        assert template_names(response)[0] == "users/user_detail.html"
        assert b"<html" in response.content
        assert b'id="user-profile"' in response.content

    def test_htmx_partial(self, user: User, client: Client):
        client.force_login(user)

        response = client.get(user.get_absolute_url(), headers=HTMX_HEADERS)

        assert response.status_code == HTTPStatus.OK
        assert template_names(response)[0] == "users/partials/user_detail.html"
        assert "base.html" not in template_names(response)
        assert b"<html" not in response.content
        assert b'id="user-profile"' in response.content
        assert "HX-Request" in response["Vary"]
