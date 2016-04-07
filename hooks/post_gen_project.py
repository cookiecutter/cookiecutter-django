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
import hashlib
import os
import random
import shutil

from cookiecutter.config import DEFAULT_CONFIG

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    # import warnings
    # warnings.warn('A secure pseudo-random number generator is not available '
    #               'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False

def get_random_string(
        length=50,
        allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)'):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    settings.SECRET_KEY)).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))

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

# 4. Copy files from /docs/ to {{ cookiecutter.repo_name }}/docs/
# copy_doc_files(PROJECT_DIRECTORY)
