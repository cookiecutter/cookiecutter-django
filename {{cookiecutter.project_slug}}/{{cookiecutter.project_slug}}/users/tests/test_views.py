import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

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

    def test_get_success_url(self, user: User, rf: RequestFactory):
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

        assert response.url == f"/users/{user.username}/"
        assert response.status_code == 302

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

        # Get the updated user by name
        updated_user = get_user_model().objects.filter(
            name=self.form_data["name"]
        )

        # assert that the name matches
        assert updated_user != []
        assert updated_user.first().name == self.form_data["name"]  # type: ignore [union-attr]

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
    def test_authenticated(self, user: User, rf: RequestFactory):
        url = reverse("users:detail", kwargs={"username": user.username})
        request = rf.get(url)

        # Add the current user to the request object
        request.user = user

        # Process request and get response
        response = UserDetailView.as_view()(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        url = reverse("users:detail", kwargs={"username": user.username})
        request = rf.get(url)

        # Add an Anonymous User to the request object
        request.user = AnonymousUser()

        # Process request and get response
        response = UserDetailView.as_view()(request, username=user.username)

        login_url = reverse(settings.LOGIN_URL)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next={url}"
