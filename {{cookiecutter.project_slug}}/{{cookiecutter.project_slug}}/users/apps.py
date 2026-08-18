from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}.users"
    verbose_name = _("Users")

    def ready(self):
        """
        Override this method in subclasses to run code when Django starts.
        """
{% if cookiecutter.use_tenants == "y" %}
        from {{ cookiecutter.project_slug }}.users import signals  # noqa: F401
{% endif %}
