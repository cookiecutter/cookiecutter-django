from ninja import Schema, ModelSchema
from {{ cookiecutter.project_slug }}.users.models import User

class UserSchema(ModelSchema):
    url: str

    class Meta:
        model = User
        exclude = ["password"]

    @staticmethod
    def resolve_url(obj):
        return obj.get_absolute_url()
