from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AppAdminSite(admin.AdminSite):
    site_title = _("{{cookiecutter.project_name}} site admin")
    site_header = _("{{cookiecutter.project_name}} administration")
