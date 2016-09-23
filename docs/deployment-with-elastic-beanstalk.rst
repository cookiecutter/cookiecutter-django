Deployment with Elastic Beanstalk
==========================================

.. index:: Elastic Beanstalk

Warning: Experimental
---------------------

This is experimental. For the time being there will be bugs and issues. If you've never used Elastic Beanstalk before, please hold off before trying this option.

On the other hand, we need help cleaning this up. If you do have knowledge of Elastic Beanstalk, we would appreciate the help. :)

Prerequisites
-------------

* awsebcli

Instructions
-------------

::

  # creates the directory of environments (servers)
  eb init -p python3.4 {{ cookiecutter.project_slug }}

  # Creates the environment (server) where the app will run
  eb create {{ cookiecutter.project_slug }}
  # Note: This will fail on a postgres error, because postgres doesn't exist yet

  # Make sure you are in the right environment
  eb list

  # If you are not in the right environment
  eb use {{ cookiecutter.project_slug }}

  # Set the environment variables
  python ebsetenv.py

  # Go to EB AWS config. Create new RDS database (postgres, 9.4.9, db.t2.micro)
  # Get some coffee, this is going to take a while

  # Deploy again
  eb deploy

  # Take a look
  eb open

FAQ
-----

Why Not Use Docker on Elastic Beanstalk?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because I didn't want to add an abstraction (Docker) on top of an abstraction (Elastic Beanstalk) on top of an abstraction (Cookiecutter Django).
