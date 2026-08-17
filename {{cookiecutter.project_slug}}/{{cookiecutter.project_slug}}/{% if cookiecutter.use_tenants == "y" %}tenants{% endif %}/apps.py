from django.apps import AppConfig


class TenantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{cookiecutter.project_slug}}.tenants"
    label = "tenants"
