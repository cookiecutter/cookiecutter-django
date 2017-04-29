from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = '{{cookiecutter.project_slug}}.utils'
    verbose_name = "Utils"

    def ready(self):
        """Override this to put in:
            Utils system checks
            Utils signal registration
        """
        pass
