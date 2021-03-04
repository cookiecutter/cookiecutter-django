import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pytest_django.asserts import assertContains, assertRedirects

from {{ cookiecutter.project_slug }}.users.models import User
from {{ cookiecutter.project_slug }}.users.views import (
    UserDetailView,
    UserRedirectView,
    UserUpdateView,
)

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    form_data = {"name": "Updated Name"}

    def test_get_success_url(self, user: User, rf: RequestFactory, client: Client):
        url = reverse("users:update")
        request = rf.post(url, self.form_data)

        # Add the session middleware to the request
        SessionMiddleware().process_request(request)

        # Add the message middleware to the request
        MessageMiddleware().process_request(request)

        # Add the current user to the request object
        request.user = user

        # Process request and get response
        response = UserUpdateView.as_view()(request)

        # Add client attribute to response object
        # required for assertRedirects
        response.client = client

        # Make User login
        response.client.force_login(user)

        # Make sure the correct url is returned with status_code 302
        # and the final constructed url page can be loaded with status_code 200
        assertRedirects(response, expected_url=f"/users/{user.username}/")

    def test_get_object(self, user: User, rf: RequestFactory):
        url = reverse("users:update")
        request = rf.get(url)
        # Add the current user to the request object
        request.user = user

        # Process request and get response
        response = UserUpdateView.as_view()(request)

        assert response.context_data["object"] == user  # type: ignore [attr-defined]

    def test_form_valid(self, user: User, rf: RequestFactory):
        url = reverse("users:update")
        request = rf.post(url, self.form_data)

        # Add the session middleware to the request
        SessionMiddleware().process_request(request)

        # Add the message middleware to the request
        MessageMiddleware().process_request(request)

        # Add the current user to the request object
        request.user = user

        # Process request and get response
        UserUpdateView.as_view()(request)

        # Get the updated user
        user.refresh_from_db()
        assert user.name == self.form_data["name"]

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [_("Information successfully updated")]


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        url = reverse("users:redirect")
        request = rf.get(url)
        # Add the current user to the request object
        request.user = user

        # Process request and get response
        response = UserRedirectView.as_view()(request)

        assert response.url == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory, client: Client):
        url = reverse("users:detail", kwargs={"username": user.username})
        request = rf.get(url)

        # Add the current user to the request object
        request.user = user

        # Process request and get response
        response = UserDetailView.as_view()(request, username=user.username)

        # Add client attribute to response object
        # required for assertRedirects
        # by default this will assume the user is not logged-in
        response.client = client

        # Make User login
        response.client.force_login(user)

        # Make sure status_code 200 is returned
        # and that the user's username appears in the response content
        assertContains(response, text=user.username)

    def test_not_authenticated(self, user: User, rf: RequestFactory, client: Client):
        # Get Login Url
        login_url = reverse(settings.LOGIN_URL)

        url = reverse("users:detail", kwargs={"username": user.username})
        request = rf.get(url)

        # Add an Anonymous User to the request object
        request.user = AnonymousUser()

        # Process request and get response
        response = UserDetailView.as_view()(request, username=user.username)

        # Add client attribute to response object
        # required for assertRedirects
        # by default this will assume the user is not logged-in
        response.client = client

        # Make sure the correct url is returned with status_code 302
        # and the final constructed url page can be loaded with status_code 200
        assertRedirects(response, expected_url=f"{login_url}?next={url}")
