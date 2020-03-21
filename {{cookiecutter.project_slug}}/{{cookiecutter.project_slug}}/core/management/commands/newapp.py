from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from pathlib import Path
from humps import pascalize

class Command(BaseCommand):
    help = 'Start a new django app using the Cookiecutter layout'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, **options):
        app_name = options.pop('app_name')
        pascal_app_name = pascalize(app_name)
        app_dir = Path(settings.APPS_DIR)
        project_slug = app_dir.stem

        call_command('startapp', app_name)

        current_app_path = Path(settings.ROOT_DIR) / app_name

        target_app_path = app_dir / app_name

        current_app_path.replace(target_app_path)

        APPS_PY = (
                'from django.apps import AppConfig\n'
                'from django.utils.translation import gettext_lazy as _'
                '\n\n\n'
                f'class {pascal_app_name}Config(AppConfig):\n'
                f'    name = {project_slug}.{app_name}\n'
                f'    verbose_name = _("{app_name}")\n\n'
                'def ready(self):\n'
                '    try:\n'
                f'        import {project_slug}.{app_name}.signals\n'
                '    except:\n'
                '        pass'
                )

        target_apps_py = target_app_path / 'apps.py'

        with target_apps_py.open('w', encoding='utf8') as apps_py:
            apps_py.write(APPS_PY)

