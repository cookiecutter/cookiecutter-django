Deployment on EBS
=================

.. index:: Amazon Elastic Beanstalk

This is still very much work in progress. Testing is needed and appreciated.

Instructions on how to get django-cookiecutter to work on Amazon Elastic Beanstalk (EBS) with Docker Multicontainer setup.

It is supposed that the developer is using AWS services:
- RDS for database
- Route 53 for DNS
- Certificate manager for HTTPS
- Elasticache for Redis caching
- IAM for access management
- S3 for file storage


CLI
-----
Install awsebcli (included in local requirements file).

Instructions can be found on
- http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
- http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-getting-started.html


Create docker images
--------------------
.. code-block:: bash
    docker build -f compose/production/django/Dockerfile -t <user>/<repo> .

Note: the dot "." in the end of the command is important!


Upload docker images
--------------------
At the time of writing, multicontainer EBS does not support uploading containers straight to AWS. You need to add the containers to a container hub.

.. code-block:: bash
    docker push <user>/<repo>


You can host your containers on the standard Docker hub, which will give you unlimited public containers and 1 private container.
You can also host your containers on a private container hub, e.g. (free tier options)
- ECR
- https://cloud.google.com/container-engine/
- https://arukas.io/en/

Docs at http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.container.console.html
You can upload a .cfg file in the S3 bucket that the Beanstalk deploy created, that way you won't have any trouble with permissions.

Update Dockerrun file
---------------------
After uploading your Docker image, you need to update your Dockerrun.aws.json file to point to the correct repository <user>/<repo>
If you are using a private repository, you need to add a configuration file to a secure S3 bucket. Info on http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.container.console.html#docker-images-private


Setup EBS
---------
Follow normal instructions for setting up an EBS instance:

.. code-block:: bash
    eb init
    eb create <repo>
    eb deploy


Set environment variables
-------------------------
Environment variables can be set in multiple ways:
- Through the CLI http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-configuration-methods-after.html#configuration-options-after-ebcli-ebsetenv
- Through the console http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-configuration-methods-after.html#configuration-options-after-console-configpage
- Through .ebextensions http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-configuration-methods-after.html#configuration-options-after-console-ebextensions


Local run
---------
You can test out your setup locally by adding "local" after the eb command
.. code-block:: bash
    eb local run

http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-local.html
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker-eblocal.html

RDS
------

You can setup RDS for your production and development usage.

* Production
It is possible to create an RDS instance through your EBS console. http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.db.html
However, it is recommended to create a RDS DB instance seperately and then link this to you EBS setup. This way both lifecycles are seperate and you can delete your EBS without losing your RDS.
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html

* Development
It is adviced to create a seperate development RDS instance for your local development.
- Go to RDS console
- Go to Instances
- Launch DB instance
- Choose PostgreSQL
- Choose Dev/Test option
- Fill out all the fields
- Wait for your database to be created
- Set all the environment variables locally. You can find the RDS_HOSTNAME as "endpoint". You do need to remove the port, as this is a separate environment variable.

Route 53
--------
- Add a hosted zone with your domain name
- Find the NS record in your hosted zone, these are nameservers
- Copy the nameservers to your DNS host

Certificate manager
-------------------
AWS provide you with free SSL certificates. Request a certificate through the Certificate Manager.

- You can add you domain to "Domain name" (e.g. example.com) and add every subdomain to "Additional names" (e.g. *.example.com).
- An email will be sent to admin@example.com to verify if you are the owner of the domain, if it is not registered through AWS.


ElastiCache
-----------
Launch a Redis instance in ElastiCache and copy the Port and Endpoint to your environment variables.

* Note: The author has only tested that "it doesn't crash". Please open a ticket if it turns out that nothing is caching.


IAM
-----
Using your root account for all AWS is a bad idea. Follow the recommendations in your "Security Status" section in the IAM dashboard.

You need following Policies attached to your user/group:
- AWSElasticBeanstalkReadOnlyAccess
- AWSElasticBeanstalkFullAccess
- AWSElasticBeanstalkService

S3
-----
As S3 is already the default for django-cookiecutter, nothing extra needs to be done here.


Useful commands
---------------
.. code-block:: bash
    eb terminate
    eb <env> setenv VAR=value


Running commands
----------------

It is possible to run django commands, such as createsuperuser.

Note: there might be better ways of doing this, PRs welcome!

You can ssh into your EBS instance:
.. code-block:: bash
    eb ssh <project_name>

Then there you can go in the correct Docker instance.
1. Find the name of the Docker instance
.. code-block:: bash
    sudo docker ps

2. Log onto the Docker instance
.. code-block:: bash
    sudo docker exec -it <docker_instance_name> bash

3. Navigate to correct folder
.. code-block:: bash
    cd /var/app/current

4. Run commands
.. code-block:: bash
    python manage.py createsuperuser



Documentation
-------------
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker_ecs.html

TODO
----

* Celery
Should Celery have it's own container? How does Celery behave when EBS boots up multiple containers, each with running Celery workers?

CELERY
https://github.com/Maxbey/socialaggregator/blob/232690ef14ffbd7735297262ab6c26717bd53f05/aws/Dockerrun.aws.json
https://github.com/pogorelov-ss/django-elastic-beanstalk-docker-stack/blob/fb1e717ec3be0b7fef99497d4e27626386da100f/Dockerrun.aws.json

* Do we need something like Supervisor on EBS?

Troubleshooting
---------------

* Package version mismatch
There are issues that come from a mismatch between docker, compose and awsebcli packages.
For awsebcli to function, you need to install docker-py outside your virtual environment.
.. code-block:: bash
    sudo pip install docker-py==1.7.2


* SECURE_SSL_REDIRECT
The author didn't get it to run on production without setting up HTTPS certificates correctly, even with SECURE_SSL_REDIRECT set to False.
