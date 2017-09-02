import os
import random
import shutil
import string

try:
    # Inspired by https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

PROJECT_DIR_PATH = os.path.realpath(os.path.curdir)


def remove_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_open_source_project_only_files() -> None:
    filenames = [
        'CONTRIBUTORS.txt'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_gplv3_files() -> None:
    filenames = [
        'COPYING'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_pycharm_files() -> None:
    idea_dir_path = os.path.join(PROJECT_DIR_PATH, '.idea')
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join(PROJECT_DIR_PATH, 'docs', 'pycharm')
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files() -> None:
    shutil.rmtree(os.path.join(PROJECT_DIR_PATH, 'compose'))

    filenames = [
        'local.yml',
        'production.yml',
        '.dockerignore'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_heroku_files() -> None:
    filenames = [
        'Procfile',
        'runtime.txt'
    ]
    for filename in filenames:
        remove_file(os.path.join(PROJECT_DIR_PATH, filename))


def remove_elasticbeanstalk_files() -> None:
    ebextensions_dir_path = os.path.join(PROJECT_DIR_PATH, '.ebextensions')
    if os.path.exists(ebextensions_dir_path):
        shutil.rmtree(ebextensions_dir_path)

    filenames = [
        'ebsetenv.py'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def try_remove_paas_files() -> None:
    none_paas_files_left = True

    if '{{ cookiecutter.use_heroku }}'.lower() != 'y':
        remove_heroku_files()
        none_paas_files_left &= True
    else:
        none_paas_files_left &= False

    if '{{ cookiecutter.use_elasticbeanstalk_experimental }}'.lower() != 'y':
        remove_elasticbeanstalk_files()
        none_paas_files_left &= True
    else:
        none_paas_files_left &= False

    if none_paas_files_left:
        remove_file(os.path.join(PROJECT_DIR_PATH, 'requirements.txt'))


def remove_grunt_files() -> None:
    filenames = [
        'Gruntfile.js'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_gulp_files() -> None:
    filenames = [
        'gulpfile.js'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_packagejson_file() -> None:
    filenames = [
        'package.json'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_celery_app() -> None:
    task_app_path = os.path.join(PROJECT_DIR_PATH, '{{ cookiecutter.project_slug }}', 'taskapp')
    shutil.rmtree(task_app_path)


def append_to_gitignore(path) -> None:
    gitignore_file_path = os.path.join(PROJECT_DIR_PATH, '.gitignore')
    with open(gitignore_file_path, 'a') as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(length: int,
                           using_digits: bool = False,
                           using_ascii_letters: bool = False,
                           using_punctuation: bool = False) -> str:
    """
    Returns a securely generated random string.
    For instance, opting out for 50 symbol-long, [a-z][A-Z][0-9] string
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
    return ''.join([random.choice(symbols) for i in range(length)])


def replace_flag_with_random_string(file_path: str,
                                    flag: str,
                                    *args,
                                    **kwargs) -> None:
    random_string = generate_random_string(*args, **kwargs)
    if random_string is None:
        print("We couldn't find a secure pseudo-random number generator on your system. "
              "Please, {} manually.".format(flag))
        random_string = flag

    with open(file_path, 'r+') as file:
        file_contents = file.read().replace(flag, random_string)
        file.seek(0)
        file.write(file_contents)
        file.truncate()


def set_django_secret_key(file_path: str) -> None:
    replace_flag_with_random_string(file_path, '!!!SET DJANGO_SECRET_KEY!!!',
                                    length=50,
                                    using_digits=True,
                                    using_ascii_letters=True,
                                    using_punctuation=True)


def set_postgres_user(file_path: str) -> None:
    replace_flag_with_random_string(file_path, '!!!SET POSTGRES_USER!!!',
                                    length=8,
                                    using_ascii_letters=True)


def set_postgres_password(file_path: str) -> None:
    replace_flag_with_random_string(file_path, '!!!SET POSTGRES_PASSWORD!!!',
                                    length=30,
                                    using_digits=True,
                                    using_ascii_letters=True)


def main():
    if '{{ cookiecutter.open_source_license }}' == 'Not open source':
        remove_open_source_project_only_files()

    if '{{ cookiecutter.open_source_license}}' != 'GPLv3':
        remove_gplv3_files()

    if '{{ cookiecutter.use_pycharm }}'.lower() != 'y':
        remove_pycharm_files()

    if '{{ cookiecutter.use_docker }}'.lower() != 'y':
        remove_docker_files()

    try_remove_paas_files()

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
            "You selected to use docker and a JS task runner. "
            "This is NOT supported out of the box for now. "
            "You can continue to use the project like you normally would, "
            "but you would need to add a JS task runner service "
            "to your Docker Compose configuration manually."
        )

    if '{{ cookiecutter.use_celery }}'.lower() == 'n':
        remove_celery_app()

    append_to_gitignore('.envs/')
    append_to_gitignore('.env')

    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'local.py'))
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'test.py'))
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, '.envs', '.production', '.django'))

    envs_local_postgres = os.path.join(PROJECT_DIR_PATH, '.envs', '.local', '.postgres')
    set_postgres_user(envs_local_postgres)
    set_postgres_password(envs_local_postgres)

    envs_production_postgres = os.path.join(PROJECT_DIR_PATH, '.envs', '.production', '.postgres')
    set_postgres_user(envs_production_postgres)
    set_postgres_password(envs_production_postgres)


if __name__ == '__main__':
    main()
