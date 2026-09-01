from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from typing import Any
from allauth.account.models import EmailAddress
from allauth.account.internal.flows.email_verification import (
    send_verification_email_to_address,
)
from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User
{%- if cookiecutter.use_django_unfold == 'y' %}
from unfold.admin import ModelAdmin
{%- endif %}

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
{%- if cookiecutter.use_django_unfold == 'y' %}
class UserAdmin(ModelAdmin,auth_admin.UserAdmin):
{%- else %}
class UserAdmin(auth_admin.UserAdmin):
{%- endif %}
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
{%- if cookiecutter.use_tenants == "y" %}
    filter_horizontal: tuple[str,...] = ()
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_verified")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ("last_login", "is_verified")
    list_display = ["email", "name", "is_active", "is_verified"]
    list_filter = ("is_active", "is_verified")
    ordering = ["email"]
    search_fields = ["name", "email"]
{%- else -%}
    fieldsets = (
        {%- if cookiecutter.username_type == "email" %}
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        {%- else %}
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        {%- endif %}
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    ordering = ["id"]
    search_fields = ["name"]
    list_display = ["{{cookiecutter.username_type}}", "name", "is_superuser"]
{%- endif %}
    {%- if cookiecutter.username_type == "email" %}
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    {%- endif %}
{% if cookiecutter.use_tenants == 'y' %}
    def delete_model(self, request, obj):
        User.objects.delete_user(obj)
{% endif %}
    def save_model(self, request: Any, obj: Model, form: Any, change: bool) -> None:
        super().save_model(
            request,
            obj,
            form,
            change,
        )

        # Only send the email when a NEW user is created.
        if change:
            return

        if not isinstance(obj, User):
            return

        if not obj.email:
            return
        email_address, created = EmailAddress.objects.get_or_create(
            user=obj,
            email=obj.email,
            defaults={
                "primary": True,
                "verified": False,
            },
        )
        if email_address.verified:
            return

        send_verification_email_to_address(
            request=request,
            address=email_address,
        )

