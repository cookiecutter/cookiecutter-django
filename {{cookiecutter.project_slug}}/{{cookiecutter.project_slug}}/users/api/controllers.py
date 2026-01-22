from typing import List

from ninja import Router
from {{ cookiecutter.project_slug }}.users.models import User
from .schema import UserSchema

router = Router()

@router.get("/", response=List[UserSchema])
def list_users(request):
    return User.objects.all()
