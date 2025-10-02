{% if cookiecutter.rest_api == 'DRF' -%}
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from {{ cookiecutter.project_slug }}.users.models import User

from .serializers import UserSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    {%- if cookiecutter.username_type == "email" %}
    lookup_field = "pk"
    {%- else %}
    lookup_field = "username"
    {%- endif %}

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
{%- elif cookiecutter.rest_api == 'Django Ninja' -%}
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja import Router

from {{ cookiecutter.project_slug }}.users.api.schema import UpdateUserSchema
from {{ cookiecutter.project_slug }}.users.api.schema import UserSchema
from {{ cookiecutter.project_slug }}.users.models import User

router = Router(tags=["users"])


def _get_users_queryset(request) -> QuerySet[User]:
    return User.objects.filter(pk=request.user.pk)


@router.get("/", response=list[UserSchema])
def list_users(request):
    return _get_users_queryset(request)
{%- if cookiecutter.username_type == "email" %}


@router.get("/{pk}/", response=UserSchema)
def retrieve_user(request, pk: str):
    if pk == "me":
        return request.user
    users_qs = _get_users_queryset(request)
    return get_object_or_404(users_qs, pk=pk)
{%- else %}


@router.get("/{username}/", response=UserSchema)
def retrieve_user(request, username: str):
    if username == "me":
        return request.user
    users_qs = _get_users_queryset(request)
    return get_object_or_404(users_qs, username=username)
{%- endif %}
{%- if cookiecutter.username_type == "email" %}


@router.patch("/{pk}/", response=UserSchema)
def update_user(request, pk: str, data: UpdateUserSchema):
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, pk=pk)
    user.name = data.name
    user.save()
    return user
{%- else %}


@router.patch("/{username}/", response=UserSchema)
def update_user(request, username: str, data: UpdateUserSchema):
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, username=username)
    user.name = data.name
    user.save()
    return user
{%- endif %}
{%- endif %}
