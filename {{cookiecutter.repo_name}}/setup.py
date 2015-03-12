#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="{{ cookiecutter.project_name }}",
    version="{{ cookiecutter.version }}",
    author="{{ cookiecutter.author_name }}",
    author_email="{{ cookiecutter.email }}",
    packages=[
        "{{ cookiecutter.repo_name }}",
    ],
    include_package_data=True,
    install_requires=[
        "Django==1.7.6",
    ],
    zip_safe=False,
    scripts=["{{ cookiecutter.repo_name }}/manage.py"],
)
