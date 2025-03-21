from django.contrib.admin.apps import AdminConfig


class AppAdminConfig(AdminConfig):
    default_site = "{{cookiecutter.project_slug}}.admin.AppAdminSite"
