from __future__ import annotations

import typing

from django.contrib.auth import get_user_model
from rest_framework import serializers

if typing.TYPE_CHECKING:
    from {{ cookiecutter.project_slug }}.users.models import User as UserType


User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        {%- if cookiecutter.username_type == "email" %}
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
        {%- else %}
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }
        {%- endif %}
