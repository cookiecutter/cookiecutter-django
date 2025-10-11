from django.urls.base import reverse
from ninja import ModelSchema

from {{ cookiecutter.project_slug }}.users.models import User


class UpdateUserSchema(ModelSchema):
    class Meta:
        model = User
        {%- if cookiecutter.username_type == "email" %}
        fields = ["name"]
        {%- else %}
        fields = ["username", "name"]
        {%- endif %}


class UserSchema(ModelSchema):
    url: str

    class Meta:
        model = User
        {%- if cookiecutter.username_type == "email" %}
        fields = ["email", "name"]
        {%- else %}
        fields = ["username", "email", "name"]
        {%- endif %}

    @staticmethod
    def resolve_url(obj: User):
        {%- if cookiecutter.username_type == "email" %}
        return reverse("api:retrieve_user", kwargs={"pk": obj.pk})
        {%- else %}
        return reverse("api:retrieve_user", kwargs={"username": obj.username})
        {%- endif %}
