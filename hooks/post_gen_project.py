# -*- coding: utf-8 -*-
import os
import shutil

project_directory = os.path.realpath(os.path.curdir)

# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
pycharm = '{{cookiecutter.use_pycharm}}' == 'y'

pycharm_files = [

]

pycharm_dirs = [
    '.idea/',
]

if not pycharm:
    for path in pycharm_files:
        os.remove(os.path.join(project_directory, path))

    for path in pycharm_dirs:
        shutil.rmtree(os.path.join(project_directory, path))

# ------------------------------------------------------------------------------


import fileinput

jdk_table_xml = os.path.join(project_directory, 'compose/pycharm/jdk.table.xml')
jdk_table_dst_dir = os.path.join(os.path.expanduser('~'), '.PyCharm40/config/options/')

for line in fileinput.input(jdk_table_xml, inplace=True):
    print line.replace('$PROJECT_DIR$', project_directory),


if not os.path.exists(jdk_table_dst_dir):
    os.makedirs(jdk_table_dst_dir)
    shutil.copy2(jdk_table_xml, jdk_table_dst_dir)
