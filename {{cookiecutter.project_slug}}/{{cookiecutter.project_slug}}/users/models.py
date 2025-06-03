import uuid as uuid_lib

{%- if cookiecutter.username_type == "email" %}
from typing import ClassVar

{% endif -%}
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
{%- if cookiecutter.username_type == "email" %}

from .managers import UserManager
{%- endif %}


class User(AbstractUser):
    """
    Default custom user model for {{cookiecutter.project_name}}.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    uuid = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    {%- if cookiecutter.username_type == "email" %}
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects: ClassVar[UserManager] = UserManager()
    {%- endif %}

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"uuid": self.uuid})

    def __str__(self):
        {%- if cookiecutter.username_type == "email" %}
        return f"{self.first_name} {self.last_name}"
        {%- else %}
        return f"{self.username}"
        {%- endif %}

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.email = self.email.lower()
        super().save(*args, **kwargs)
