import pytest
from django.test import RequestFactory

from {{ cookiecutter.project_slug }}.users.api.serializers import UserSerializer
from {{ cookiecutter.project_slug }}.users.api.views import UserViewSet
from {{ cookiecutter.project_slug }}.users.models import User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username, 
            "email": user.email, 
            "name": user.name, 
            "url": f"/api/users/{user.username}/",
        }
