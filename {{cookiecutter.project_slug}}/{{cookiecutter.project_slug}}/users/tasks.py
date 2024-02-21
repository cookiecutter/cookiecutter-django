from config import celery_app
from {{ cookiecutter.project_slug }}.users.models import User


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
