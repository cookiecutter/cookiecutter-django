from django.apps import AppConfig


class DomainConfig(AppConfig):
    name = '{{cookiecutter.project_slug}}.domain'
    verbose_name = "Domain"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
