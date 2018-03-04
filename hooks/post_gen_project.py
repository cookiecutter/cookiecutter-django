"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""

import os
import random
import shutil
import string
import sys

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

PROJECT_DIR_PATH = os.path.realpath(os.path.curdir)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


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
        remove_file(os.path.join(PROJECT_DIR_PATH, file_name))




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
             *args,
             **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            import sys
            sys.stdout.write(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
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
        length=50,
        using_digits=True,
        using_ascii_letters=True
    )
    return django_secret_key


def set_postgres_user(file_path,
                      value=None):
    postgres_user = set_flag(
        file_path,
        '!!!SET POSTGRES_USER!!!',
        value=value,
        length=8,
        using_ascii_letters=True
    )
    return postgres_user


def set_postgres_password(file_path):
    postgres_password = set_flag(
        file_path,
        '!!!SET POSTGRES_PASSWORD!!!',
        length=42,
        using_digits=True,
        using_ascii_letters=True
    )
    return postgres_password


def initialize_dotenv(postgres_user):
    # Initializing `env.example` first.
    envexample_file_path = os.path.join(PROJECT_DIR_PATH, 'env.example')
    set_django_secret_key(envexample_file_path)
    set_postgres_user(envexample_file_path, value=postgres_user)
    set_postgres_password(envexample_file_path)
    # Renaming `env.example` to `.env`.
    dotenv_file_path = os.path.join(PROJECT_DIR_PATH, '.env')
    shutil.move(envexample_file_path, dotenv_file_path)


def initialize_localyml(postgres_user):
    set_postgres_user(os.path.join(PROJECT_DIR_PATH, 'local.yml'), value=postgres_user)


def initialize_local_settings():
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'local.py'))


def initialize_test_settings():
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'test.py'))


def main():
    postgres_user = generate_random_string(length=16, using_ascii_letters=True)
    initialize_dotenv(postgres_user)
    initialize_localyml(postgres_user)
    initialize_local_settings()
    initialize_test_settings()

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
        TERMINATOR = "\x1b[0m"
        INFO = "\x1b[1;33m [INFO]: "
        sys.stdout.write(
            INFO +
            "Docker and {} JS task runner ".format('{{ cookiecutter.js_task_runner }}'.lower().capitalize()) +
            "working together not supported yet. "
            "You can continue using the generated project like you normally would, "
            "however you would need to add a JS task runner service "
            "to your Docker Compose configuration manually." +
            TERMINATOR
        )

    if '{{ cookiecutter.use_celery }}'.lower() == 'n':
        remove_celery_app()


if __name__ == '__main__':
    main()
