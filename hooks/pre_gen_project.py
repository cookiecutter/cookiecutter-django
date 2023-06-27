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

# The content of this string is evaluated by Jinja, and plays an important role.
# It updates the cookiecutter context to trim leading and trailing spaces
# from domain/email values
"""
{{ cookiecutter.update({ "domain_name": cookiecutter.domain_name | trim }) }}
{{ cookiecutter.update({ "email": cookiecutter.email | trim }) }}
"""

project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert project_slug.isidentifier(), "'{}' project slug is not a valid Python identifier.".format(project_slug)

assert project_slug == project_slug.lower(), "'{}' project slug should be all lowercase".format(project_slug)

assert "\\" not in "{{ cookiecutter.author_name }}", "Don't include backslashes in author name."

if "{{ cookiecutter.use_docker }}".lower() == "n":
    python_major_version = sys.version_info[0]
    if python_major_version == 2:
        print(
            WARNING + "You're running cookiecutter under Python 2, but the generated "
            "project requires Python 3.11+. Do you want to proceed (y/n)? " + TERMINATOR
        )
        yes_options, no_options = frozenset(["y"]), frozenset(["n"])
        while True:
            choice = raw_input().lower()  # noqa: F821
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

if "{{ cookiecutter.use_whitenoise }}".lower() == "n" and "{{ cookiecutter.cloud_provider }}" == "None":
    print("You should either use Whitenoise or select a " "Cloud Provider to serve static files")
    sys.exit(1)

if "{{ cookiecutter.mail_service }}" == "Amazon SES" and "{{ cookiecutter.cloud_provider }}" != "AWS":
    print("You should either use AWS or select a different " "Mail Service for sending emails.")
    sys.exit(1)
