from ninja import Schema, ModelSchema
from {{ cookiecutter.project_slug }}.users.models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "name", "url"]
        extra = "readonly"

    url: str
