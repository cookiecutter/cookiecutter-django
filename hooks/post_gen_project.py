# -*- coding: utf-8 -*-
import os
import shutil

project_directory = os.path.realpath(os.path.curdir)

docker = '{{cookiecutter.use_docker}}' == 'y'

docker_files = [
    'debug.yml',
    'dev.yml',
    'docker-compose.yml',
    'Dockerfile'
]

docker_dirs = [
    'compose/',
]

if not docker:
    for path in docker_files:
        os.remove(os.path.join(project_directory, path))

    for path in docker_dirs:
        shutil.rmtree(os.path.join(project_directory, path))
