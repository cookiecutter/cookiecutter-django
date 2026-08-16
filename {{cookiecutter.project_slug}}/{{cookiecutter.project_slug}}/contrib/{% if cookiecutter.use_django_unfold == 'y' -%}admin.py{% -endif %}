from unfold.admin import ModelAdmin
from allauth.mfa.models import Authenticator
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialToken
from django.contrib.auth.models import Group
from django.contrib import admin
from allauth.account.models import EmailAddress

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    filter_horizontal: tuple[str, ...] = ("permissions",)

admin.site.unregister(EmailAddress)
@admin.register(EmailAddress)
class EmailAddressAdmin(ModelAdmin):
    list_display = [
        "email",
        "user",
        "verified",
        "primary",
    ]

    list_filter = [
        "verified",
        "primary",
    ]

    search_fields = [
        "email",
        "user__email",
    ]

admin.site.unregister(Authenticator)
@admin.register(Authenticator)
class AuthenticatorAdmin(ModelAdmin):
    list_display = [
        "user",
        "type",
        "created_at",
    ]

    list_filter = [
        "type",
    ]

    search_fields = [
        "user__email",
    ]

admin.site.unregister(SocialAccount)
@admin.register(SocialAccount)
class SocialAccountAdmin(ModelAdmin):
    list_display = [
        "user",
        "provider",
        "uid",
    ]

    list_filter = [
        "provider",
    ]

    search_fields = [
        "user__email",
        "uid",
    ]

admin.site.unregister(SocialApp)
@admin.register(SocialApp)
class SocialAppAdmin(ModelAdmin):
    list_display = [
        "name",
        "provider",
        "client_id",
    ]

    list_filter = [
        "provider",
    ]

    search_fields = [
        "name",
        "provider",
        "client_id",
    ]

admin.site.unregister(SocialToken)
@admin.register(SocialToken)
class SocialTokenAdmin(ModelAdmin):
    list_display = [
        "account",
        "app",
        "expires_at",
    ]

    list_filter = [
        "app",
    ]

    search_fields = [
        "account__user__email",
    ]
