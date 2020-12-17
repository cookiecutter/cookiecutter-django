#!/usr/bin/env python

import shlex
import subprocess  # nosec
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Our version ALWAYS matches the version of Django we support
# If Django has a new release, we branch, tag, then update this setting after the tag.
version = "3.0.11"


def run_command(command):
    args = shlex.split(command, posix=False)
    return subprocess.check_output(args, shell=False)  # nosec


if sys.argv[-1] == "tag":
    run_command('git tag -a {version} -m "version {version}"'.format(version=version))
    run_command("git push --tags")
    sys.exit(0)

with open("README.rst") as readme_file:
    long_description = readme_file.read()

setup(
    name="cookiecutter-django",
    version=version,
    description="A Cookiecutter template for creating production-ready Django projects quickly.",
    long_description=long_description,
    author="Daniel Roy Greenfeld",
    author_email="pydanny@gmail.com",
    url="https://github.com/pydanny/cookiecutter-django",
    packages=[],
    license="BSD",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
    ],
    keywords=(
        "cookiecutter, Python, projects, project templates, django, "
        "skeleton, scaffolding, project directory, setup.py"
    ),
)
