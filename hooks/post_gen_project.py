"""
Does the following:

1. Generates and saves random secret key
2. Removes the taskapp if celery isn't going to be used
3. Removes the .idea directory if PyCharm isn't going to be used
4. Copy files from /docs/ to {{ cookiecutter.project_slug }}/docs/

    TODO: this might have to be moved to a pre_gen_hook

A portion of this code was adopted from Django's standard crypto functions and
utilities, specifically:
    https://github.com/django/django/blob/master/django/utils/crypto.py
"""
import os
import random
import shutil
import string

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', '').replace("'", '')
    punctuation = punctuation.replace('\\', '')
    if using_sysrandom:
        return ''.join(random.choice(
            string.digits + string.ascii_letters + punctuation
        ) for i in range(length))

    print(
        "Cookiecutter Django couldn't find a secure pseudo-random number generator on your system."
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


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def remove_task_app(project_directory):
    """Removes the taskapp if celery isn't going to be used"""
    # Determine the local_setting_file_location
    task_app_location = os.path.join(
        PROJECT_DIRECTORY,
        '{{ cookiecutter.project_slug }}/taskapp'
    )
    shutil.rmtree(task_app_location)


def remove_pycharm_dir(project_directory):
    """
    Removes directories related to PyCharm
    if it isn't going to be used
    """
    idea_dir_location = os.path.join(PROJECT_DIRECTORY, '.idea/')
    if os.path.exists(idea_dir_location):
        shutil.rmtree(idea_dir_location)

    docs_dir_location = os.path.join(PROJECT_DIRECTORY, 'docs/pycharm/')
    if os.path.exists(docs_dir_location):
        shutil.rmtree(docs_dir_location)


def remove_heroku_files():
    """
    Removes files needed for heroku if it isn't going to be used
    """
    filenames = ["Procfile", "runtime.txt"]
    if '{{ cookiecutter.use_elasticbeanstalk_experimental }}'.lower() != 'y':
        filenames.append("requirements.txt")
    for filename in ["Procfile", "runtime.txt"]:
        file_name = os.path.join(PROJECT_DIRECTORY, filename)
        remove_file(file_name)


def remove_docker_files():
    """
    Removes files needed for docker if it isn't going to be used
    """
    for filename in ["local.yml", "production.yml", ".dockerignore"]:
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
    for filename in ["Gruntfile.js"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

def remove_gulp_files():
    """
    Removes files needed for grunt if it isn't going to be used
    """
    for filename in ["gulpfile.js"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

def remove_packageJSON_file():
    """
    Removes files needed for grunt if it isn't going to be used
    """
    for filename in ["package.json"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))


def remove_copying_files():
    """
    Removes files needed for the GPLv3 licence if it isn't going to be used
    """
    for filename in ["COPYING"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

def remove_elasticbeanstalk():
    """
    Removes elastic beanstalk components
    """
    docs_dir_location = os.path.join(PROJECT_DIRECTORY, '.ebextensions')
    if os.path.exists(docs_dir_location):
        shutil.rmtree(docs_dir_location)

    filenames = ["ebsetenv.py", ]
    if '{{ cookiecutter.use_heroku }}'.lower() != 'y':
        filenames.append("requirements.txt")
    for filename in filenames:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

def remove_open_source_files():
    """
    Removes files conventional to opensource projects only.
    """
    for filename in ["CONTRIBUTORS.txt"]:
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

# Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

# Removes the taskapp if celery isn't going to be used
if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_task_app(PROJECT_DIRECTORY)

# Removes the .idea directory if PyCharm isn't going to be used
if '{{ cookiecutter.use_pycharm }}'.lower() != 'y':
    remove_pycharm_dir(PROJECT_DIRECTORY)

# Removes all heroku files if it isn't going to be used
if '{{ cookiecutter.use_heroku }}'.lower() != 'y':
    remove_heroku_files()

# Removes all docker files if it isn't going to be used
if '{{ cookiecutter.use_docker }}'.lower() != 'y':
    remove_docker_files()

# Removes all JS task manager files if it isn't going to be used
if '{{ cookiecutter.js_task_runner}}'.lower() == 'gulp':
    remove_grunt_files()
elif '{{ cookiecutter.js_task_runner}}'.lower() == 'grunt':
    remove_gulp_files()
else:
    remove_gulp_files()
    remove_grunt_files()
    remove_packageJSON_file()

# Display a warning if use_docker and use_grunt are selected. Grunt isn't
#   supported by our docker config atm.
if '{{ cookiecutter.js_task_runner }}'.lower() in ['grunt', 'gulp'] and '{{ cookiecutter.use_docker }}'.lower() == 'y':
    print(
        "You selected to use docker and a JS task runner. This is NOT supported out of the box for now. You "
        "can continue to use the project like you normally would, but you will need to add a "
        "js task runner service to your docker configuration manually."
    )


# Removes files needed for the GPLv3 licence if it isn't going to be used.
if '{{ cookiecutter.open_source_license}}' != 'GPLv3':
    remove_copying_files()

# Remove Elastic Beanstalk files
if '{{ cookiecutter.use_elasticbeanstalk_experimental }}'.lower() != 'y':
    remove_elasticbeanstalk()

# Remove files conventional to opensource projects only.
if '{{ cookiecutter.open_source_license }}' == 'Not open source':
    remove_open_source_files()
