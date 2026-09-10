{% if cookiecutter.rest_api == 'DRF' -%}
from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from {{ cookiecutter.project_slug }}.users.models import User

from .serializers import UserSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from {{ cookiecutter.project_slug }}.typedefs import AuthenticatedApiRequest


class UserViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet[User],
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # ``IsAuthenticated`` is the default permission class (config/settings/base.py).
    request: AuthenticatedApiRequest
    {%- if cookiecutter.username_type == "email" %}
    lookup_field = "pk"
    {%- else %}
    lookup_field = "username"
    {%- endif %}

    def get_queryset(self) -> QuerySet[User]:
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request: AuthenticatedApiRequest) -> Response:
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
{%- elif cookiecutter.rest_api == 'Django Ninja' -%}
# Annotations stay evaluated at runtime (no ``from __future__ import annotations``)
# because django-ninja reads them to build the OpenAPI schema and validate input.
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja import Router

from {{ cookiecutter.project_slug }}.typedefs import AuthenticatedHttpRequest
from {{ cookiecutter.project_slug }}.users.api.schema import UpdateUserSchema
from {{ cookiecutter.project_slug }}.users.api.schema import UserSchema
from {{ cookiecutter.project_slug }}.users.models import User

router = Router(tags=["users"])


def _get_users_queryset(request: AuthenticatedHttpRequest) -> QuerySet[User]:
    return User.objects.filter(pk=request.user.pk)


@router.get("/", response=list[UserSchema])
def list_users(request: AuthenticatedHttpRequest) -> QuerySet[User]:
    return _get_users_queryset(request)
{%- if cookiecutter.username_type == "email" %}


@router.get("/me/", response=UserSchema)
def retrieve_current_user(request: AuthenticatedHttpRequest) -> User:
    return request.user


@router.get("/{pk}/", response=UserSchema)
def retrieve_user(request: AuthenticatedHttpRequest, pk: int) -> User:
    users_qs = _get_users_queryset(request)
    return get_object_or_404(users_qs, pk=pk)
{%- else %}


@router.get("/me/", response=UserSchema)
def retrieve_current_user(request: AuthenticatedHttpRequest) -> User:
    return request.user


@router.get("/{username}/", response=UserSchema)
def retrieve_user(request: AuthenticatedHttpRequest, username: str) -> User:
    users_qs = _get_users_queryset(request)
    return get_object_or_404(users_qs, username=username)
{%- endif %}


@router.patch("/me/", response=UserSchema)
def update_current_user(
    request: AuthenticatedHttpRequest,
    data: UpdateUserSchema,
) -> User:
    user = request.user
    if data.name is not None:
        user.name = data.name
    {%- if cookiecutter.username_type == "username" %}
    user.username = data.username
    {%- endif %}
    user.save()
    return user
{%- if cookiecutter.username_type == "email" %}


@router.patch("/{pk}/", response=UserSchema)
def update_user(
    request: AuthenticatedHttpRequest,
    pk: int,
    data: UpdateUserSchema,
) -> User:
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, pk=pk)
    if data.name is not None:
        user.name = data.name
    user.save()
    return user
{%- else %}


@router.patch("/{username}/", response=UserSchema)
def update_user(
    request: AuthenticatedHttpRequest,
    username: str,
    data: UpdateUserSchema,
) -> User:
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, username=username)
    if data.name is not None:
        user.name = data.name
    user.username = data.username
    user.save()
    return user
{%- endif %}
{%- endif %}
