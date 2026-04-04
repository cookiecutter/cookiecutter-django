from __future__ import annotations

from factory import Faker
from factory import post_generation
from factory.django import DjangoModelFactory

from {{ cookiecutter.project_slug }}.users.models import User


class UserFactory(DjangoModelFactory[User]):
    {%- if cookiecutter.username_type == "username" %}
    username = Faker("user_name")
    {%- endif %}
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self: User, create: bool, extracted: str | None, **kwargs):  # noqa: FBT001
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)
        if create:
            self.save()

    class Meta:
        model = User
        django_get_or_create = ["{{cookiecutter.username_type}}"]
        skip_postgeneration_save = True

{%- if cookiecutter.username_type == "phone" %}
# ── Phone user factory ────────────────────────────────────────────────────────
import factory
from factory.django import DjangoModelFactory
from factory import post_generation
from collections.abc import Sequence
from typing import Any


class UserFactory(DjangoModelFactory):
    phone = factory.Sequence(lambda n: f"+1555{n:07d}")
    phone_verified = False
    name = factory.Faker("name")
    email = factory.Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):  # noqa: FBT001
        if extracted:
            self.set_password(extracted)
            if create:
                self.save(update_fields=["password"])
        # default: leave unusable password

    class Meta:
        model = "users.User"
        django_get_or_create = ["phone"]
{%- endif %}
