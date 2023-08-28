from django.contrib.auth import get_user_model
from rest_framework import serializers

from {{ cookiecutter.project_slug }}.users.models import User as UserType


User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["email", "uuid", "first_name", "last_name", "url"]
        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "uuid"}}
