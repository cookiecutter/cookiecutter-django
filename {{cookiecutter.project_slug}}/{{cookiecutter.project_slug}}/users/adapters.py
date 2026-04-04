from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

    from {{cookiecutter.project_slug}}.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

{%- if cookiecutter.username_type == "phone" %}

    # ------------------------------------------------------------------ #
    # Phone storage — allauth 65.x delegates all model I/O to the adapter #
    # ------------------------------------------------------------------ #

    def get_phone(self, user) -> tuple[str, bool] | None:
        """Return (phone, verified) tuple or None if the user has no phone."""
        phone = getattr(user, "phone", None)
        if phone:
            return phone, user.phone_verified
        return None

    def set_phone(self, user, phone: str, verified: bool) -> None:
        """Persist phone number and verified status on the user model."""
        user.phone = phone
        user.phone_verified = verified
        user.save(update_fields=["phone", "phone_verified"])

    def set_phone_verified(self, user, phone: str) -> None:
        """Mark the phone number as verified after successful OTP check."""
        user.phone_verified = True
        user.save(update_fields=["phone_verified"])

    def get_user_by_phone(self, phone: str):
        """Look up a user by phone number for login. Returns None if not found."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

    # ------------------------------------------------------------------ #
    # SMS sending — fill in your provider below                           #
    # ------------------------------------------------------------------ #

    def send_verification_code_sms(self, user, phone: str, code: str, **kwargs) -> None:
        """
        Send the OTP code to `phone` via SMS.

        Replace the logger.warning() call with your SMS provider:

        ── Twilio ────────────────────────────────────────────────────────
        from django.conf import settings
        from twilio.rest import Client
        Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN).messages.create(
            body=f"Your {{ cookiecutter.project_name }} code: {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone,
        )

        ── Vonage / Nexmo ────────────────────────────────────────────────
        import vonage
        from django.conf import settings
        vonage.Sms(vonage.Client(key=settings.VONAGE_API_KEY,
                                 secret=settings.VONAGE_API_SECRET)).send_message(
            {"from": settings.VONAGE_BRAND_NAME, "to": phone.lstrip("+"), "text": f"Code: {code}"}
        )
        """
        import logging
        # TODO: replace with your SMS provider — see docstring above
        logging.getLogger(__name__).warning(
            "send_verification_code_sms() not implemented. "
            "OTP code for %s: %s  ← use this during development",
            phone, code,
        )

    def send_unknown_account_sms(self, phone: str, **kwargs) -> None:
        """Called when enumeration-prevention is on and the phone has no account."""
        import logging
        logging.getLogger(__name__).warning(
            "send_unknown_account_sms() not implemented for %s.", phone
        )

{%- endif %}


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = super().populate_user(request, sociallogin, data)
        if not user.name:
            if name := data.get("name"):
                user.name = name
            elif first_name := data.get("first_name"):
                user.name = first_name
                if last_name := data.get("last_name"):
                    user.name += f" {last_name}"
        return user
