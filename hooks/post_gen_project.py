# -*- coding: utf-8 -*-
import os
import shutil

project_directory = os.path.realpath(os.path.curdir)

if '{{cookiecutter.use_pycharm}}' != 'y':
    shutil.rmtree(os.path.join(project_directory, '.idea/'))

docker_private_key = 'compose/debug/keys_to_docker/id_rsa'
os.chmod(os.path.join(project_directory, docker_private_key), 0600)
