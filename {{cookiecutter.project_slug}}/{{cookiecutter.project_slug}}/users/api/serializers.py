from rest_framework import serializers

from {{ cookiecutter.project_slug }}.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["email", "uuid", "first_name", "last_name", "url"]
        extra_kwargs = {"url": {"view_name": "api:user-detail", "lookup_field": "uuid"}}
