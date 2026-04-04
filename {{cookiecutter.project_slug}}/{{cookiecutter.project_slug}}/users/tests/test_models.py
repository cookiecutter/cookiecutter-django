from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from {{ cookiecutter.project_slug }}.users.models import User


def test_user_get_absolute_url(user: User):
    {%- if cookiecutter.username_type == "email" %}
    assert user.get_absolute_url() == f"/users/{user.pk}/"
    {%- else %}
    assert user.get_absolute_url() == f"/users/{user.username}/"
    {%- endif %}

{%- if cookiecutter.username_type == "phone" %}


class TestPhoneUserModel:
    def test_user_get_absolute_url(self, user):
        assert user.get_absolute_url() == f"/users/{user.pk}/"

    def test_new_user_has_unusable_password(self, db):
        from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory
        user = UserFactory()
        assert not user.has_usable_password()

    def test_user_can_have_optional_password(self, db):
        from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory
        user = UserFactory(password="SecretPass123!")  # noqa: S106
        assert user.has_usable_password()

    def test_phone_is_unique(self, db):
        import pytest
        from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory
        UserFactory(phone="+12125550001")
        with pytest.raises(Exception):
            UserFactory(phone="+12125550001")
{%- endif %}
