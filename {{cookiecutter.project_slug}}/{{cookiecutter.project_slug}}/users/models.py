{%- if cookiecutter.username_type in ("email", "phone") %}
from typing import ClassVar

{% endif -%}
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField
from django.db.models import CharField
{%- if cookiecutter.username_type in ("email", "phone") %}
from django.db.models import EmailField
{%- endif %}
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
{%- if cookiecutter.username_type in ("email", "phone") %}

from .managers import UserManager
{%- endif %}


class User(AbstractUser):
    """
    Default custom user model for {{cookiecutter.project_name}}.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    {%- if cookiecutter.username_type == "email" %}
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
    {%- elif cookiecutter.username_type == "phone" %}
    # Phone is the primary login identifier, stored in E.164 format e.g. +12125552368
    username = None  # type: ignore[assignment]
    phone = CharField(
        _("Phone Number"),
        max_length=17,
        unique=True,
        help_text=_("Required. E.164 format: +[country code][number]"),
    )
    phone_verified = BooleanField(_("Phone Verified"), default=False)
    # Email is optional for phone-auth users — they can add one later
    email = EmailField(_("email address"), blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def save(self, *args, **kwargs):
        """New users start with an unusable password; they can set one later."""
        if self._state.adding and not self.has_usable_password():
            self.set_unusable_password()
        super().save(*args, **kwargs)
    {%- endif %}

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        {%- if cookiecutter.username_type in ("email", "phone") %}
        return reverse("users:detail", kwargs={"pk": self.id})
        {%- else %}
        return reverse("users:detail", kwargs={"username": self.username})
        {%- endif %}
