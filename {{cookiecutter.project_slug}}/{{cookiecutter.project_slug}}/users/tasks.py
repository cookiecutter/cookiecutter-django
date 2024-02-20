from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
