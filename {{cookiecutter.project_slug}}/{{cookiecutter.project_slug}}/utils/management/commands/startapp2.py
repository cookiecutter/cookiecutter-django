import os
import shutil
from importlib import import_module
from os import path

import django
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.core.management.utils import handle_extensions
from django.template import Context, Engine
from django.utils.version import get_docs_version

# Setup a stub settings environment for template rendering
from django.conf import settings

if not settings.configured:
    settings.configure()

COOKIECUTTER_DJANGO_APPS_PATH = str(settings.APPS_DIR)
COOKIECUTTER_DJANGO_APPS_DIR_NAME = os.path.basename(COOKIECUTTER_DJANGO_APPS_PATH)
COOKIECUTTER_DJANGO_BASE_SETTINGS_FILE = str(settings.ROOT_DIR.path('config', 'settings', 'base.py'))


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the {dir}/ directory.".format(dir=COOKIECUTTER_DJANGO_APPS_PATH)
    )
    missing_args_message = "You must provide an application name."

    def add_arguments(self, parser):
        parser.add_argument('name', help='Name of the application or project.')
        # parser.add_argument('directory', nargs='?', help='Optional destination directory')
        parser.add_argument('--template',
                            help='The path or URL to load the template from.')
        parser.add_argument('--extension', '-e', dest='extensions',
                            action='append', default=['py'],
                            help='The file extension(s) to render (default: "py"). '
                                 'Separate multiple extensions with commas, or use '
                                 '-e multiple times.')
        parser.add_argument('--name', '-n', dest='files',
                            action='append', default=[],
                            help='The file name(s) to render. '
                                 'Separate multiple extensions with commas, or use '
                                 '-n multiple times.')

    def handle(self, **options):
        name = options.pop('name')
        self.app_or_project = 'app'
        self.paths_to_remove = []
        self.verbosity = options['verbosity']

        self.validate_name(name, self.app_or_project)
        dot_path_base_name = '{}.{}'.format(COOKIECUTTER_DJANGO_APPS_DIR_NAME, name)
        # Check that the app_name cannot be imported.
        try:
            import_module(dot_path_base_name)
        except ImportError:
            pass
        else:
            raise CommandError(
                "%r conflicts with the name of an existing Python module and "
                "cannot be used as an app name. Please try another name." % name
            )

        top_dir = path.join(COOKIECUTTER_DJANGO_APPS_PATH, name)
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise CommandError("'%s' already exists" % top_dir)
        except OSError as e:
            raise CommandError(e)

        extensions = tuple(handle_extensions(options['extensions']))
        extra_files = []
        for file in options['files']:
            extra_files.extend(map(lambda x: x.strip(), file.split(',')))
        if self.verbosity >= 2:
            self.stdout.write("Rendering %s template files with "
                              "extensions: %s\n" %
                              (self.app_or_project, ', '.join(extensions)))
            self.stdout.write("Rendering %s template files with "
                              "filenames: %s\n" %
                              (self.app_or_project, ', '.join(extra_files)))

        base_name = '%s_name' % self.app_or_project
        base_subdir = '%s_template' % self.app_or_project
        base_directory = '%s_directory' % self.app_or_project
        camel_case_name = 'camel_case_%s_name' % self.app_or_project
        camel_case_value = ''.join(x for x in name.title() if x != '_')

        context = Context(dict(options, **{
            base_name: dot_path_base_name,
            base_directory: top_dir,
            camel_case_name: camel_case_value,
            'docs_version': get_docs_version(),
            'django_version': django.__version__,
        }), autoescape=False)

        template_dir = self.handle_template(options['template'],
                                            base_subdir)
        prefix_length = len(template_dir) + 1

        for root, dirs, files in os.walk(template_dir):

            path_rest = root[prefix_length:]
            relative_dir = path_rest.replace(base_name, name)
            if relative_dir:
                target_dir = path.join(top_dir, relative_dir)
                if not path.exists(target_dir):
                    os.mkdir(target_dir)

            for dirname in dirs[:]:
                if dirname.startswith('.') or dirname == '__pycache__':
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith(('.pyo', '.pyc', '.py.class')):
                    # Ignore some files as they cause various breakages.
                    continue
                old_path = path.join(root, filename)
                new_path = path.join(top_dir, relative_dir,
                                     filename.replace(base_name, name))
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path = new_path[:-len(old_suffix)] + new_suffix
                        break  # Only rewrite once

                if path.exists(new_path):
                    raise CommandError("%s already exists, overlaying a "
                                       "project or app into an existing "
                                       "directory won't replace conflicting "
                                       "files" % new_path)

                # Only render the Python files, as we don't want to
                # accidentally render Django templates files
                if new_path.endswith(extensions) or filename in extra_files:
                    with open(old_path, 'r', encoding='utf-8') as template_file:
                        content = template_file.read()
                    template = Engine().from_string(content)
                    content = template.render(context)
                    with open(new_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(content)
                else:
                    shutil.copyfile(old_path, new_path)

                if self.verbosity >= 2:
                    self.stdout.write("Creating %s\n" % new_path)
                try:
                    shutil.copymode(old_path, new_path)
                    self.make_writeable(new_path)
                except OSError:
                    self.stderr.write(
                        "Notice: Couldn't set permission bits on %s. You're "
                        "probably using an uncommon filesystem setup. No "
                        "problem." % new_path, self.style.NOTICE)

        if self.paths_to_remove:
            if self.verbosity >= 2:
                self.stdout.write("Cleaning up temporary files.\n")
            for path_to_remove in self.paths_to_remove:
                if path.isfile(path_to_remove):
                    os.remove(path_to_remove)
                else:
                    shutil.rmtree(path_to_remove)

        msg = "'{dot_path_base_name}.apps.{camel_case_value}Config',".format(dot_path_base_name=dot_path_base_name,
                                                                             camel_case_value=camel_case_value)
        self.stdout.write(
            'please, add:\n\n{}\n\nto your LOCAL_APPS on {}\n'.format(msg, COOKIECUTTER_DJANGO_BASE_SETTINGS_FILE))
