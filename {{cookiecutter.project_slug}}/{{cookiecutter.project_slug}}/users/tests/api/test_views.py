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
