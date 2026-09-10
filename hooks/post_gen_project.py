# ruff: noqa: PLR0133
import os
import random
import shutil
import string
import subprocess
import sys
from pathlib import Path

try:
    # Inspired by
    # https://github.com/django/django/blob/main/django/utils/crypto.py
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
        Path(file_name).unlink()


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        Path(file_name).unlink()


def remove_custom_user_manager_files():
    users_path = Path("{{cookiecutter.project_slug}}", "users")
    (users_path / "managers.py").unlink()
    (users_path / "tests" / "test_managers.py").unlink()


def remove_pycharm_files():
    idea_dir_path = Path(".idea")
    if idea_dir_path.exists():
        shutil.rmtree(idea_dir_path)

    docs_dir_path = Path("docs", "pycharm")
    if docs_dir_path.exists():
        shutil.rmtree(docs_dir_path)


def remove_docker_files():
    shutil.rmtree(".devcontainer")
    shutil.rmtree("compose")

    file_names = [
        "docker-compose.local.yml",
        "docker-compose.production.yml",
        ".dockerignore",
        "justfile",
    ]
    for file_name in file_names:
        Path(file_name).unlink()
    if "{{ cookiecutter.editor }}" == "PyCharm":
        file_names = ["docker_compose_up_django.xml", "docker_compose_up_docs.xml"]
        for file_name in file_names:
            Path(".idea", "runConfigurations", file_name).unlink()


def remove_nginx_docker_files():
    shutil.rmtree(Path("compose", "production", "nginx"))


def remove_utility_files():
    shutil.rmtree("utility")


def remove_heroku_files():
    file_names = ["Procfile"]
    for file_name in file_names:
        if file_name == "requirements.txt" and "{{ cookiecutter.ci_tool }}".lower() == "travis":
            # Don't remove the file if we are using Travis CI but not using Heroku
            continue
        Path(file_name).unlink()
    shutil.rmtree("bin")


def remove_celery_files():
    file_paths = [
        Path("config", "celery_app.py"),
        Path("{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        Path("{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"),
    ]
    for file_path in file_paths:
        file_path.unlink()


def remove_async_files():
    file_paths = [
        Path("config", "asgi.py"),
        Path("config", "websocket.py"),
    ]
    for file_path in file_paths:
        file_path.unlink()


def remove_dottravisyml_file():
    Path(".travis.yml").unlink()


def remove_dotgitlabciyml_file():
    Path(".gitlab-ci.yml").unlink()


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def remove_dotdrone_file():
    Path(".drone.yml").unlink()


def generate_random_string(length, using_digits=False, using_ascii_letters=False, using_punctuation=False):  # noqa: FBT002
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


def set_flag(file_path: Path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                f"system. Please, make sure to manually {flag} later.",
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with file_path.open("r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path: Path):
    return set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_django_admin_url(file_path: Path):
    return set_flag(
        file_path,
        "!!!SET DJANGO_ADMIN_URL!!!",
        formatted="{}/",
        length=32,
        using_digits=True,
        using_ascii_letters=True,
    )


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):  # noqa: FBT002
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    return set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)


def set_postgres_password(file_path, value=None):
    return set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_celery_flower_user(file_path, value):
    return set_flag(file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value)


def set_celery_flower_password(file_path, value=None):
    return set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def append_to_gitignore_file(ignored_line):
    with Path(".gitignore").open("a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):  # noqa: FBT002
    local_django_envs_path = Path(".envs", ".local", ".django")
    production_django_envs_path = Path(".envs", ".production", ".django")
    local_postgres_envs_path = Path(".envs", ".local", ".postgres")
    production_postgres_envs_path = Path(".envs", ".production", ".postgres")

    set_django_secret_key(production_django_envs_path)
    set_django_admin_url(production_django_envs_path)

    set_postgres_user(local_postgres_envs_path, value=postgres_user)
    set_postgres_password(local_postgres_envs_path, value=DEBUG_VALUE if debug else None)
    set_postgres_user(production_postgres_envs_path, value=postgres_user)
    set_postgres_password(production_postgres_envs_path, value=DEBUG_VALUE if debug else None)

    set_celery_flower_user(local_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(local_django_envs_path, value=DEBUG_VALUE if debug else None)
    set_celery_flower_user(production_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(production_django_envs_path, value=DEBUG_VALUE if debug else None)


def set_flags_in_settings_files():
    set_django_secret_key(Path("config", "settings", "local.py"))
    set_django_secret_key(Path("config", "settings", "test.py"))


def remove_envs_and_associated_files():
    shutil.rmtree(".envs")
    Path("merge_production_dotenvs_in_dotenv.py").unlink()
    shutil.rmtree("tests")


def remove_celery_compose_dirs():
    shutil.rmtree(Path("compose", "local", "django", "celery"))
    shutil.rmtree(Path("compose", "production", "django", "celery"))


def remove_aws_dockerfile():
    shutil.rmtree(Path("compose", "production", "aws"))


def remove_drf_starter_files():
    Path("config", "api_router.py").unlink()
    Path("{{cookiecutter.project_slug}}", "users", "api", "serializers.py").unlink()


def remove_ninja_starter_files():
    Path("config", "api.py").unlink()
    Path("{{cookiecutter.project_slug}}", "users", "api", "schema.py").unlink()


def remove_rest_api_files():
    remove_drf_starter_files()
    remove_ninja_starter_files()
    shutil.rmtree(Path("{{cookiecutter.project_slug}}", "users", "api"))
    shutil.rmtree(Path("{{cookiecutter.project_slug}}", "users", "tests", "api"))


def main():  # noqa: C901, PLR0912, PLR0915
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

    if "{{ cookiecutter.username_type }}" == "username":
        remove_custom_user_manager_files()

    if "{{ cookiecutter.editor }}" != "PyCharm":
        remove_pycharm_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        remove_utility_files()
        if "{{ cookiecutter.cloud_provider }}".lower() != "none":
            remove_nginx_docker_files()
    else:
        remove_docker_files()

    if "{{ cookiecutter.use_docker }}".lower() == "y" and "{{ cookiecutter.cloud_provider}}" != "AWS":
        remove_aws_dockerfile()

    if "{{ cookiecutter.use_heroku }}".lower() == "n":
        remove_heroku_files()

    if "{{ cookiecutter.use_docker }}".lower() == "n" and "{{ cookiecutter.use_heroku }}".lower() == "n":
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            print(
                INFO + ".env(s) are only utilized when Docker Compose and/or "
                "Heroku support is enabled. Keeping them as requested, but they may not be useful "
                "in your current setup." + TERMINATOR,
            )
        else:
            remove_envs_and_associated_files()
    else:
        append_to_gitignore_file(".env")
        append_to_gitignore_file(".envs/*")
        if "{{ cookiecutter.keep_local_envs_in_vcs }}".lower() == "y":
            append_to_gitignore_file("!.envs/.local/")

    if "{{ cookiecutter.cloud_provider }}" == "None" and "{{ cookiecutter.use_docker }}".lower() == "n":
        print(
            WARNING + "You chose to not use any cloud providers nor Docker, "
            "media files won't be served in production." + TERMINATOR,
        )

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()
        if "{{ cookiecutter.use_docker }}".lower() == "y":
            remove_celery_compose_dirs()

    if "{{ cookiecutter.ci_tool }}" != "Travis":
        remove_dottravisyml_file()

    if "{{ cookiecutter.ci_tool }}" != "Gitlab":
        remove_dotgitlabciyml_file()

    if "{{ cookiecutter.ci_tool }}" != "Github":
        remove_dotgithub_folder()

    if "{{ cookiecutter.ci_tool }}" != "Drone":
        remove_dotdrone_file()

    if "{{ cookiecutter.rest_api }}" == "DRF":
        remove_ninja_starter_files()
    elif "{{ cookiecutter.rest_api }}" == "Django Ninja":
        remove_drf_starter_files()
    else:
        remove_rest_api_files()

    if "{{ cookiecutter.use_async }}".lower() == "n":
        remove_async_files()

    setup_dependencies()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


def setup_dependencies():
    print("Installing python dependencies using uv...")

    if "{{ cookiecutter.use_docker }}".lower() == "y":
        # Build a trimmed down Docker image add dependencies with uv
        uv_docker_image_path = Path("compose/local/uv/Dockerfile")
        uv_image_tag = "cookiecutter-django-uv-runner:latest"
        try:
            subprocess.run(  # noqa: S603
                [  # noqa: S607
                    "docker",
                    "build",
                    "--load",
                    "-t",
                    uv_image_tag,
                    "-f",
                    str(uv_docker_image_path),
                    "-q",
                    ".",
                ],
                check=True,
                env={
                    **os.environ,
                    "DOCKER_BUILDKIT": "1",
                },
            )
        except subprocess.CalledProcessError as e:
            print(f"Error building Docker image: {e}", file=sys.stderr)
            sys.exit(1)

        current_path = Path.cwd().absolute()
        # Use Docker to run the uv command
        uv_cmd = ["docker", "run", "--rm", "-v", f"{current_path}:/app", uv_image_tag, "uv"]
    else:
        # Use uv command directly
        uv_cmd = ["uv"]

    # Install production dependencies
    try:
        subprocess.run([*uv_cmd, "add", "--no-sync", "-r", "requirements/production.txt"], check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error installing production dependencies: {e}", file=sys.stderr)
        sys.exit(1)

    # Install local (development) dependencies
    try:
        subprocess.run([*uv_cmd, "add", "--no-sync", "--dev", "-r", "requirements/local.txt"], check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error installing local dependencies: {e}", file=sys.stderr)
        sys.exit(1)

    # Remove the requirements directory
    requirements_dir = Path("requirements")
    if requirements_dir.exists():
        try:
            shutil.rmtree(requirements_dir)
        except Exception as e:  # noqa: BLE001
            print(f"Error removing 'requirements' folder: {e}", file=sys.stderr)
            sys.exit(1)

    uv_image_parent_dir_path = Path("compose/local/uv")
    if uv_image_parent_dir_path.exists():
        shutil.rmtree(str(uv_image_parent_dir_path))

    print("Setup complete!")


if __name__ == "__main__":
    main()
