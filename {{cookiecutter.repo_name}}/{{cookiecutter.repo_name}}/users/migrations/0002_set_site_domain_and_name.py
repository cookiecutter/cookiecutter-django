# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
from django.apps import apps as django_apps


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    Site = django_apps.get_model("sites", "Site")
    site = Site.objects.get(id=settings.SITE_ID)
    site.domain = "{{cookiecutter.domain_name}}"
    site.name = "{{cookiecutter.project_name}}"
    site.save()


def update_site_backward(apps, schema_editor):
    """Revert site domain and name to default."""
    Site = django_apps.get_model("sites", "Site")
    site = Site.objects.get(id=settings.SITE_ID)
    site.domain = 'example.com'
    site.name = 'example.com'
    site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
