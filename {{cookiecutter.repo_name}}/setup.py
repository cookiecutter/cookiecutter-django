#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import {{ cookiecutter.repo_name }}
version = {{ cookiecutter.repo_name }}.__version__

setup(
    name='{{ cookiecutter.project_name }}',
    version=version,
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    packages=[
        '{{ cookiecutter.repo_name }}',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['{{ cookiecutter.repo_name }}/manage.py'],
)
