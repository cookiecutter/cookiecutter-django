Testing and Contiinuous Deployment with GitLab CI
=================================================

Prerequisites
-------------

* Docker and Docker Compose (minimum versions in Deployment with Docker)
* Docker Machine for continuous deployment (tested with 0.5.5)

Configuring GitLab CI to Run the Tests
--------------------------------------

1) Set up an Ubuntu machine with Docker.  Digital Ocean has a droplet configuration
that makes this very convenient but any machine will do.

2) Install docker-compose according to the docs:

::

    curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

2) Install docker-machine according to the docs:

::

    curl -L https://github.com/docker/machine/releases/download/v0.5.5/docker-machine_linux-amd64 > /usr/local/bin/docker-machine
    chmod +x /usr/local/bin/docker-machine

3) Install and register gitlab-ci-multi-runner according to the docs.  When registering,
use the shell executor:

::

    curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-ci-multi-runner/script.deb.sh | sudo bash
    apt-get install gitlab-ci-multi-runner
    gitlab-runner register # Use shell executor.

4) Add the gitlab-runner user account to the docker group:

::

    usermod -aG docker gitlab-runner

At ths point, GitLab CI is capable of running the tests.  Continue on below to
set up continuous deployment.

Configuring GitLab CI for Continuous Deployment
-----------------------------------------------

1) Set up an Ubuntu machine with Docker for the production site.  Digital Ocean
has a droplet configuration that makes this very convenient but any machine will do.

2) On the test runner, create an ssh key.  Add it as an authorized key on the
production machine and as a deploy key in the GitLab project:

::

    sudo -u gitlab-runner -H ssh-keygen -t rsa -C "gitlab-runner@DOMAIN"

4) On the test runner, create a docker machine for the production site:

::

    sudo -u gitlab-runner -H docker-machine create -d generic --generic-ip-address <IP address of production site> {{cookiecutter.domain_name}}

All Done
--------

Congratulations!  You now have a GitLab CI environment to run the tests for
every commit (all branches including feature branches) and automatically deploy
the master branch to the production site.

