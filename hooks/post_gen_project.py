# -*- coding: utf-8 -*-
import os
import shutil

project_directory = os.path.realpath(os.path.curdir)

def clean(items):
    for item in items:
        path = os.path.join(project_directory, item)
        if os.path.isdir(path):
           shutil.rmtree(path)
        else:
            os.remove(path)

pycharm = '{{cookiecutter.use_pycharm}}' == 'y'
docker = '{{cookiecutter.use_docker}}' == 'y'

# ------------------------------------------------------------------------------
docker_files = [
    'debug.yml',
    'dev.yml',
    'docker-compose.yml',
    'Dockerfile',
    'compose/',
]

if not docker:
    clean(docker_files)
# ------------------------------------------------------------------------------
pycharm_files = [
    '.idea/',
]

pycharm_docker_files = [
    '.idea/Docker__createsuperuser.xml',
    '.idea/Docker__grunt_build.xml',
    '.idea/Docker__grunt_compass.xml',
    '.idea/Docker__grunt_serve.xml',
    '.idea/Docker__grunt_start_email_server.xml',
    '.idea/Docker__grunt_stop_email_server.xml',
    '.idea/Docker__grunt_watch.xml',
    '.idea/Docker__migrate.xml',
    '.idea/Docker__runserver_plus.xml',
    '.idea/Docker__runserver.xml',
    '.idea/Docker__tests___all.xml',
    '.idea/Docker__tests___class__TestUser.xml',
    '.idea/Docker__tests___file__test_models.xml',
    '.idea/Docker__tests___module__users.xml',
    '.idea/Docker__tests___specific__test_get_absolute_url.xml',
    '.idea/Docker__tests___users.xml',
]

if not pycharm:
    clean(pycharm_files)
elif pycharm and not docker:
    clean(pycharm_docker_files)
# ------------------------------------------------------------------------------
