# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = {{ cookiecutter.repo_name }}.__version__

setup(
    name='{{ cookiecutter.project_name }}',
    version=version,
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    packages=[
        '{{ cookiecutter.project_name }}',
    ],
    include_package_data=True,
    install_requires=[
    ],
    zip_safe=False,
    scripts=['manage.py'],
)
