"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

PROJECT_DIR_PATH = os.path.realpath(os.path.curdir)  # TODO: ? I doubt even need that


def remove_open_source_project_only_files():
    file_names = [
        'CONTRIBUTORS.txt',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_gplv3_files():
    file_names = [
        'COPYING',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_pycharm_files():
    idea_dir_path = os.path.join(PROJECT_DIR_PATH, '.idea')
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join(PROJECT_DIR_PATH, 'docs', 'pycharm')
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    shutil.rmtree(os.path.join(PROJECT_DIR_PATH, 'compose'))

    file_names = [
        'local.yml',
        'production.yml',
        '.dockerignore',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_heroku_files():
    file_names = [
        'Procfile',
        'runtime.txt',
        'requirements.txt',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_grunt_files():
    file_names = [
        'Gruntfile.js',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_gulp_files():
    file_names = [
        'gulpfile.js',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_packagejson_file():
    file_names = [
        'package.json',
    ]
    for file_name in file_names:
        os.remove(os.path.join(PROJECT_DIR_PATH, file_name))


def remove_celery_app():
    shutil.rmtree(os.path.join(PROJECT_DIR_PATH, '{{ cookiecutter.project_slug }}', 'taskapp'))


def remove_dottravisyml_file():
    os.remove(os.path.join(PROJECT_DIR_PATH, '.travis.yml'))


def append_to_project_gitignore(path):
    gitignore_file_path = os.path.join(PROJECT_DIR_PATH, '.gitignore')
    with open(gitignore_file_path, 'a') as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(length,
                           using_digits=False,
                           using_ascii_letters=False,
                           using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        symbols += string.punctuation \
            .replace('"', '') \
            .replace("'", '') \
            .replace('\\', '')
    return ''.join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path,
             flag,
             value=None,
             formatted=None,
             *args,
             **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, 'r+') as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        '!!!SET DJANGO_SECRET_KEY!!!',
        length=64,
        using_digits=True,
        using_ascii_letters=True
    )
    return django_secret_key


def set_django_admin_url(file_path):
    django_admin_url = set_flag(
        file_path,
        '!!!SET DJANGO_ADMIN_URL!!!',
        formatted='^{}/',
        length=32,
        using_digits=True,
        using_ascii_letters=True
    )
    return django_admin_url


def generate_postgres_user():
    return generate_random_string(
        length=32,
        using_ascii_letters=True
    )


def set_postgres_user(file_path,
                      value=None):
    postgres_user = set_flag(
        file_path,
        '!!!SET POSTGRES_USER!!!',
        value=value or generate_postgres_user()
    )
    return postgres_user


def set_postgres_password(file_path):
    postgres_password = set_flag(
        file_path,
        '!!!SET POSTGRES_PASSWORD!!!',
        length=64,
        using_digits=True,
        using_ascii_letters=True
    )
    return postgres_password


def append_to_gitignore_file(s):
    with open(os.path.join(PROJECT_DIR_PATH, '.gitignore'), 'a') as gitignore_file:
        gitignore_file.write(s)
        gitignore_file.write(os.linesep)


def set_flags_in_envs(postgres_user):
    local_postgres_envs_path = os.path.join(PROJECT_DIR_PATH, '.envs', '.local', '.postgres')
    set_postgres_user(local_postgres_envs_path, value=postgres_user)
    set_postgres_password(local_postgres_envs_path)

    production_django_envs_path = os.path.join(PROJECT_DIR_PATH, '.envs', '.production', '.django')
    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)

    production_postgres_envs_path = os.path.join(PROJECT_DIR_PATH, '.envs', '.production', '.postgres')
    set_postgres_user(production_postgres_envs_path, value=postgres_user)
    set_postgres_password(production_postgres_envs_path)


def set_flags_in_settings_files():
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'local.py'))
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'test.py'))


def remove_envs_and_associated_files():
    shutil.rmtree('.envs')
    os.remove('merge_production_dotenvs_in_dotenv.py')


def main():
    postgres_user = generate_postgres_user()
    set_flags_in_envs(postgres_user)
    set_flags_in_settings_files()

    if '{{ cookiecutter.open_source_license }}' == 'Not open source':
        remove_open_source_project_only_files()
    if '{{ cookiecutter.open_source_license}}' != 'GPLv3':
        remove_gplv3_files()

    if '{{ cookiecutter.use_pycharm }}'.lower() == 'n':
        remove_pycharm_files()

    if '{{ cookiecutter.use_docker }}'.lower() == 'n':
        remove_docker_files()

    if '{{ cookiecutter.use_heroku }}'.lower() == 'n':
        remove_heroku_files()

    envs_make_sense = '{{ cookiecutter.use_docker }}'.lower() == 'n' \
                      and '{{ cookiecutter.use_heroku }}'.lower() == 'n'
    if envs_make_sense:
        if '{{ cookiecutter.keep_local_envs_in_vcs }}'.lower() == 'y':
            print(
                INFO +
                ".env(s) are only utilized when Docker Compose and/or "
                "Heroku support is enabled so keeping them does not "
                "make sense given your current setup." +
                TERMINATOR
            )
        remove_envs_and_associated_files()
    else:
        append_to_gitignore_file('.env')
        append_to_gitignore_file('.envs' + '/**/*')
        if '{{ cookiecutter.keep_local_envs_in_vcs }}'.lower() == 'y':
            append_to_gitignore_file('!.envs/.local/')

    if '{{ cookiecutter.js_task_runner}}'.lower() == 'gulp':
        remove_grunt_files()
    elif '{{ cookiecutter.js_task_runner}}'.lower() == 'grunt':
        remove_gulp_files()
    else:
        remove_gulp_files()
        remove_grunt_files()
        remove_packagejson_file()
    if '{{ cookiecutter.js_task_runner }}'.lower() in ['grunt', 'gulp'] \
        and '{{ cookiecutter.use_docker }}'.lower() == 'y':
        print(
            WARNING +
            "Docker and {} JS task runner ".format(
                '{{ cookiecutter.js_task_runner }}'
                    .lower()
                    .capitalize()
            ) +
            "working together not supported yet. "
            "You can continue using the generated project like you "
            "normally would, however you would need to add a JS "
            "task runner service to your Docker Compose configuration "
            "manually." +
            TERMINATOR
        )

    if '{{ cookiecutter.use_celery }}'.lower() == 'n':
        remove_celery_app()

    if '{{ cookiecutter.use_travisci }}'.lower() == 'n':
        remove_dottravisyml_file()

    print(
        SUCCESS +
        "Project initialized, keep up the good work!" +
        TERMINATOR
    )


if __name__ == '__main__':
    main()
