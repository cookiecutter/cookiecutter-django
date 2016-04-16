"""
Does the following:

1. Generates and saves random secret key
2. Removes the taskapp if celery isn't going to be used
3. Removes the .idea directory if PyCharm isn't going to be used
4. Copy files from /docs/ to {{ cookiecutter.repo_name }}/docs/

    TODO: this might have to be moved to a pre_gen_hook

A portion of this code was adopted from Django's standard crypto functions and
utilities, specifically:
    https://github.com/django/django/blob/master/django/utils/crypto.py
"""
from __future__ import print_function
import os
import random
import shutil

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(
        length=50,
        allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)'):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if using_sysrandom:
        return ''.join(random.choice(allowed_chars) for i in range(length))
    print(
        "cookiecutter-django couldn't find a secure pseudo-random number generator on your system."
        " Please change change your SECRET_KEY variables in conf/settings/local.py and env.example"
        " manually."
    )
    return "CHANGEME!!"


def set_secret_key(setting_file_location):
    # Open locals.py
    with open(setting_file_location) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace('CHANGEME!!!', SECRET_KEY, 1)

    # Write the results to the locals.py module
    with open(setting_file_location, 'w') as f:
        f.write(file_)


def make_secret_key(project_directory):
    """Generates and saves random secret key"""
    # Determine the local_setting_file_location
    local_setting = os.path.join(
        project_directory,
        'config/settings/local.py'
    )

    # local.py settings file
    set_secret_key(local_setting)

    env_file = os.path.join(
        project_directory,
        'env.example'
    )

    # env.example file
    set_secret_key(env_file)


def remove_task_app(project_directory):
    """Removes the taskapp if celery isn't going to be used"""
    # Determine the local_setting_file_location
    task_app_location = os.path.join(
        PROJECT_DIRECTORY,
        '{{ cookiecutter.repo_name }}/taskapp'
    )
    shutil.rmtree(task_app_location)


def remove_pycharm_dir(project_directory):
    """
    Removes directories related to PyCharm
    if it isn't going to be used
    """
    idea_dir_location = os.path.join(PROJECT_DIRECTORY, '.idea/')
    shutil.rmtree(idea_dir_location)

    docs_dir_location = os.path.join(PROJECT_DIRECTORY, 'docs/pycharm/')
    shutil.rmtree(docs_dir_location)


def remove_heroku_files():
    """
    Removes files needed for heroku if it isn't going to be used
    """
    for filename in ["app.json", "Procfile", "requirements.txt", "runtime.txt"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))


def remove_docker_files():
    """
    Removes files needed for docker if it isn't going to be used
    """
    for filename in ["dev.yml", "docker-compose.yml", ".dockerignore"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY, "compose"
    ))


def remove_grunt_files():
    """
    Removes files needed for grunt if it isn't going to be used
    """
    for filename in ["Gruntfile.js", "package.json"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

# IN PROGRESS
# def copy_doc_files(project_directory):
#     cookiecutters_dir = DEFAULT_CONFIG['cookiecutters_dir']
#     cookiecutter_django_dir = os.path.join(
#         cookiecutters_dir,
#         'cookiecutter-django',
#         'docs'
#     )
#     target_dir = os.path.join(
#         project_directory,
#         'docs'
#     )
#     for name in os.listdir(cookiecutter_django_dir):
#         if name.endswith('.rst') and not name.startswith('index'):
#             src = os.path.join(cookiecutter_django_dir, name)
#             dst = os.path.join(target_dir, name)
#             shutil.copyfile(src, dst)

# 1. Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

# 2. Removes the taskapp if celery isn't going to be used
if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_task_app(PROJECT_DIRECTORY)

# 3. Removes the .idea directory if PyCharm isn't going to be used
if '{{ cookiecutter.use_pycharm }}'.lower() != 'y':
    remove_pycharm_dir(PROJECT_DIRECTORY)

# 4. Removes all heroku files if it isn't going to be used
if '{{ cookiecutter.use_heroku }}'.lower() != 'y':
    remove_heroku_files()

# 5. Removes all docker files if it isn't going to be used
if '{{ cookiecutter.use_docker }}'.lower() != 'y':
    remove_docker_files()

# 6. Removes all grunt files if it isn't going to be used
if '{{ cookiecutter.use_grunt }}'.lower() != 'y':
    remove_grunt_files()


# 7. Display a warning if use_docker and use_grunt are selected. Grunt isn't supported by our
# docker config atm.
if '{{ cookiecutter.use_grunt }}'.lower() == 'y' and '{{ cookiecutter.use_docker }}'.lower() == 'y':
    print(
        "You selected to use docker and grunt. This is NOT supported out of the box for now. You "
        "can continue to use the project like you normally would, but you will need to add a "
        " grunt service to your docker configuration manually."
    )

# 7. Display a warning if use_docker and use_mailhog are selected. Mailhog isn't supported by our
# docker config atm.
if '{{ cookiecutter.use_mailhog }}'.lower() == 'y' and '{{ cookiecutter.use_docker }}'.lower() == 'y':
    print(
        "You selected to use docker and mailhog. This is NOT supported out of the box for now. You"
        " can continue to use the project like you normally would, but you will need to add a "
        " mailhog service to your docker configuration manually."
    )

# 4. Copy files from /docs/ to {{ cookiecutter.repo_name }}/docs/
# copy_doc_files(PROJECT_DIRECTORY)
