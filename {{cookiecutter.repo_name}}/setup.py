# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import {{ cookiecutter.project_name }}
version = {{ cookiecutter.project_name }}.__version__

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
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['{{ cookiecutter.project_name }}/manage.py'],
)
