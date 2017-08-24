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


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_open_source_project_only_files():
    filenames = [
        'CONTRIBUTORS.txt'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_gplv3_files():
    filenames = [
        'COPYING'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_pycharm_files():
    idea_dir_path = os.path.join(PROJECT_DIR_PATH, '.idea')
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join(PROJECT_DIR_PATH, 'docs', 'pycharm')
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    shutil.rmtree(os.path.join(PROJECT_DIR_PATH, 'compose'))

    filenames = [
        'local.yml',
        'production.yml',
        '.dockerignore'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_heroku_files():
    filenames = [
        'Procfile',
        'runtime.txt'
    ]
    for filename in filenames:
        remove_file(os.path.join(PROJECT_DIR_PATH, filename))


def remove_elasticbeanstalk_files():
    ebextensions_dir_path = os.path.join(PROJECT_DIR_PATH, '.ebextensions')
    if os.path.exists(ebextensions_dir_path):
        shutil.rmtree(ebextensions_dir_path)

    filenames = [
        'ebsetenv.py'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def try_remove_paas_files():
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


def remove_grunt_files():
    filenames = [
        'Gruntfile.js'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_gulp_files():
    filenames = [
        'gulpfile.js'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_packagejson_file():
    filenames = [
        'package.json'
    ]
    for filename in filenames:
        os.remove(os.path.join(PROJECT_DIR_PATH, filename))


def remove_celery_app():
    task_app_path = os.path.join(PROJECT_DIR_PATH, '{{ cookiecutter.project_slug }}', 'taskapp')
    shutil.rmtree(task_app_path)


def append_to_gitignore(path):
    gitignore_file_path = os.path.join(PROJECT_DIR_PATH, '.gitignore')
    with open(gitignore_file_path, 'a') as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', '').replace("'", '')
    punctuation = punctuation.replace('\\', '')
    if using_sysrandom:
        symbols = [random.choice(string.digits + string.ascii_letters + punctuation)
                   for i in range(length)]
        return ''.join(symbols)

    print(
        "Cookiecutter Django couldn't find a secure pseudo-random number generator on your system. "
        "Please set your SECRET_KEY variables manually."
    )
    return "CHANGEME!!!"


def set_secret_key(file_path):
    with open(file_path) as file:
        file_contents = file.read()
    SECRET_KEY = generate_random_string()
    file_contents = file_contents.replace('CHANGEME!!!', SECRET_KEY, 1)
    with open(file_path, 'w') as file:
        file.write(file_contents)


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

    set_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'local.py'))
    set_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'test.py'))
    set_secret_key(os.path.join(PROJECT_DIR_PATH, '.envs', '.production', '.django'))


if __name__ == '__main__':
    main()
