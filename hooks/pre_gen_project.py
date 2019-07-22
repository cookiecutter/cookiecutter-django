"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

project_slug = "{{ cookiecutter.project_slug }}"
if hasattr(project_slug, "isidentifier"):
    assert (
        project_slug.isidentifier()
    ), "'{}' project slug is not a valid Python identifier.".format(project_slug)

assert (
    project_slug == project_slug.lower()
), "'{}' project slug should be all lowercase".format(project_slug)

assert (
    "\\" not in "{{ cookiecutter.author_name }}"
), "Don't include backslashes in author name."
