from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = "{{cookiecutter.project_slug}}.users"
    verbose_name = "Users"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
