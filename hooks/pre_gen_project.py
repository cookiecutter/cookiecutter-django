"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.

TODO: restrict Cookiecutter Django project initialization
      to Python 3.x environments only
"""

from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def check_project_slug(slug):
    assert slug.isidentifier(), f"'{slug}' project slug is not a valid Python identifier."
    assert slug == slug.lower(), f"'{slug}' project slug should be all lowercase"


def check_author_name(author_name):
    assert "\\" not in author_name, "Don't include backslashes in author name."


def check_python_version(use_docker):
    if use_docker.lower() == "n":
        python_major_version = sys.version_info[0]
        if python_major_version == 2:
            print(
                WARNING + "You're running cookiecutter under Python 2, but the generated "
                "project requires Python 3.11+. Do you want to proceed (y/n)? " + TERMINATOR
            )
            yes_options, no_options = frozenset(["y"]), frozenset(["n"])
            while True:
                choice = input().lower()
                if choice in yes_options:
                    break
                elif choice in no_options:
                    print(INFO + "Generation process stopped as requested." + TERMINATOR)
                    sys.exit(1)
                else:
                    print(
                        HINT
                        + "Please respond with {} or {}: ".format(
                            ", ".join(["'{}'".format(o) for o in yes_options if not o == ""]),
                            ", ".join(["'{}'".format(o) for o in no_options if not o == ""]),
                        )
                        + TERMINATOR
                    )


def check_whitenoise_and_cloud_provider(use_whitenoise, cloud_provider):
    if use_whitenoise.lower() == "n" and cloud_provider == "None":
        print("You should either use Whitenoise or select a Cloud Provider to serve static files")
        sys.exit(1)


def check_mail_service_and_cloud_provider(mail_service, cloud_provider):
    if mail_service == "Amazon SES" and cloud_provider != "AWS":
        print("You should either use AWS or select a different Mail Service for sending emails.")
        sys.exit(1)


if __name__ == "__main__":
    project_slug = "{{ cookiecutter.project_slug }}"
    check_project_slug(project_slug)

    author_name = "{{ cookiecutter.author_name }}"
    check_author_name(author_name)

    check_python_version("{{ cookiecutter.use_docker }}")

    check_whitenoise_and_cloud_provider("{{ cookiecutter.use_whitenoise }}", "{{ cookiecutter.cloud_provider }}")

    check_mail_service_and_cloud_provider("{{ cookiecutter.mail_service }}", "{{ cookiecutter.cloud_provider }}")
