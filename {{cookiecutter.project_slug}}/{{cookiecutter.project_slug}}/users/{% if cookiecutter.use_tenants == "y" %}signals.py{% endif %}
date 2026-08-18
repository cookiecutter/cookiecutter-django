from allauth.account.signals import (
    email_changed,
    email_confirmed,
)
from django.dispatch import receiver

from .models import User


@receiver(email_confirmed)
def on_email_confirmed(
    request,
    email_address,
    **kwargs,
):
    User.objects.filter(
        pk=email_address.user_id,
    ).update(
        email=email_address.email,
        is_verified=True,
    )


@receiver(email_changed)
def on_email_changed(
    request,
    user,
    from_email_address,
    to_email_address,
    **kwargs,
):
    User.objects.filter(
        pk=user.pk,
    ).update(
        email=to_email_address.email,
        is_verified=False,
    )