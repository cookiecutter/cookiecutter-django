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

DEBUG_VALUE = "debug"


def remove_open_source_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)


def remove_pycharm_files():
    idea_dir_path = ".idea"
    if os.path.exists(idea_dir_path):
        shutil.rmtree(idea_dir_path)

    docs_dir_path = os.path.join("docs", "pycharm")
    if os.path.exists(docs_dir_path):
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    shutil.rmtree("compose")

    file_names = ["local.yml", "production.yml", ".dockerignore"]
    for file_name in file_names:
        os.remove(file_name)


def remove_utility_files():
    shutil.rmtree("utility")


def remove_heroku_files():
    file_names = ["Procfile", "runtime.txt", "requirements.txt"]
    for file_name in file_names:
        if (
            file_name == "requirements.txt"
            and "{{ cookiecutter.ci_tool }}".lower() == "travis"
        ):
            # don't remove the file if we are using travisci but not using heroku
            continue
        os.remove(file_name)
    remove_heroku_build_hooks()


def remove_heroku_build_hooks():
    shutil.rmtree("bin")


def remove_gulp_files():
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        os.remove(file_name)


def remove_packagejson_file():
    file_names = ["package.json"]
    for file_name in file_names:
        os.remove(file_name)


def remove_celery_files():
    file_names = [
        os.path.join("config", "celery_app.py"),
        os.path.join("{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        os.path.join(
            "{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"
        ),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_async_files():
    file_names = [
        os.path.join("config", "asgi.py"),
        os.path.join("config", "websocket.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_dottravisyml_file():
    os.remove(".travis.yml")


def remove_dotgitlabciyml_file():
    os.remove(".gitlab-ci.yml")


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def append_to_project_gitignore(path):
    gitignore_file_path = ".gitignore"
    with open(gitignore_file_path, "a") as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
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
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
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

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key


def set_django_admin_url(file_path):
    django_admin_url = set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_admin_url


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    postgres_user = set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)
    return postgres_user


def set_postgres_password(file_path, value=None):
    postgres_password = set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return postgres_password


def set_celery_flower_user(file_path, value):
    celery_flower_user = set_flag(
        file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value
    )
    return celery_flower_user


def set_celery_flower_password(file_path, value=None):
    celery_flower_password = set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return celery_flower_password


def append_to_gitignore_file(s):
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(s)
        gitignore_file.write(os.linesep)


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):
    local_django_envs_path = os.path.join(".envs", ".local", ".django")
    production_django_envs_path = os.path.join(".envs", ".production", ".django")
    local_postgres_envs_path = os.path.join(".envs", ".local", ".postgres")
    production_postgres_envs_path = os.path.join(".envs", ".production", ".postgres")

    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)

    set_postgres_user(local_postgres_envs_path, value=postgres_user)
    set_postgres_password(
        local_postgres_envs_path, value=DEBUG_VALUE if debug else None
    )
    set_postgres_user(production_postgres_envs_path, value=postgres_user)
    set_postgres_password(
        production_postgres_envs_path, value=DEBUG_VALUE if debug else None
    )

    set_celery_flower_user(local_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(
        local_django_envs_path, value=DEBUG_VALUE if debug else None
    )
    set_celery_flower_user(production_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(
        production_django_envs_path, value=DEBUG_VALUE if debug else None
    )


def set_flags_in_settings_files():
    set_django_secret_key(os.path.join("config", "settings", "local.py"))
    set_django_secret_key(os.path.join("config", "settings", "test.py"))


def remove_envs_and_associated_files():
    shutil.rmtree(".envs")
    os.remove("merge_production_dotenvs_in_dotenv.py")


def remove_celery_compose_dirs():
    shutil.rmtree(os.path.join("compose", "local", "django", "celery"))
    shutil.rmtree(os.path.join("compose", "production", "django", "celery"))


def remove_node_dockerfile():
    shutil.rmtree(os.path.join("compose", "local", "node"))


def remove_aws_dockerfile():
    shutil.rmtree(os.path.join("compose", "production", "aws"))


def remove_drf_starter_files():
    os.remove(os.path.join("config", "api_router.py"))
    shutil.rmtree(os.path.join("{{cookiecutter.project_slug}}", "users", "api"))
    os.remove(
        os.path.join(
            "{{cookiecutter.project_slug}}", "users", "tests", "test_drf_urls.py"
        )
    )
    os.remove(
        os.path.join(
            "{{cookiecutter.project_slug}}", "users", "tests", "test_drf_views.py"
        )
    )


def remove_storages_module():
    os.remove(os.path.join("{{cookiecutter.project_slug}}", "utils", "storages.py"))


def main():
    debug = "{{ cookiecutter.debug }}".lower() == "y"

    set_flags_in_envs(
        DEBUG_VALUE if debug else generate_random_user(),
        DEBUG_VALUE if debug else generate_random_user(),
        debug=debug,
    )
    set_flags_in_settings_files()

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.use_pycharm }}".lower() == "n":
        remove_pycharm_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        remove_utility_files()
    else:
        remove_docker_files()

    if (
        "{{ cookiecutter.use_docker }}".lower() == "y"
        and "{{ cookiecutter.cloud_provider}}".lower() != "aws"
    ):
        remove_aws_dockerfile()

    if "{{ cookiecutter.use_heroku }}".lower() == "n":
        remove_heroku_files()
    elif "{{ cookiecutter.use_compressor }}".lower() == "n":
        remove_heroku_build_hooks()

    if (
        "{{ cookiecutter.use_docker }}".lower() == "n"
        and "{{ cookiecutter.use_heroku }}".lower() == "n"
    ):
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            print(
                INFO + ".env(s) are only utilized when Docker Compose and/or "
                "Heroku support is enabled so keeping them does not "
                "make sense given your current setup." + TERMINATOR
            )
        remove_envs_and_associated_files()
    else:
        append_to_gitignore_file(".env")
        append_to_gitignore_file(".envs/*")
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            append_to_gitignore_file("!.envs/.local/")

    if "{{ cookiecutter.js_task_runner}}".lower() == "none":
        remove_gulp_files()
        remove_packagejson_file()
        if "{{ cookiecutter.use_docker }}".lower() == "y":
            remove_node_dockerfile()

    if "{{ cookiecutter.cloud_provider}}".lower() == "none":
        print(
            WARNING + "You chose not to use a cloud provider, "
            "media files won't be served in production." + TERMINATOR
        )
        remove_storages_module()

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()
        if "{{ cookiecutter.use_docker }}".lower() == "y":
            remove_celery_compose_dirs()

    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        remove_dottravisyml_file()

    if "{{ cookiecutter.ci_tool }}".lower() != "gitlab":
        remove_dotgitlabciyml_file()

    if "{{ cookiecutter.ci_tool }}".lower() != "github":
        remove_dotgithub_folder()

    if "{{ cookiecutter.use_drf }}".lower() == "n":
        remove_drf_starter_files()

    if "{{ cookiecutter.use_async }}".lower() == "n":
        remove_async_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
