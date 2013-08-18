cookiecutter-dj-project
=======================

A cookiecutter_ template for Django.

.. _cookiecutter: https://github.com/audreyr/cookiecutter

Features
---------

* Cutting edge: For Django 1.6 and other bleeding edge stuff
* Twitter Bootstrap 3
* Registration via django-allauth
* User avatars via django-avatar
* Procfile for deploying to Heroku
* Heroku optimized requirements
* Basic caching setup

Constraints
-----------

* Only maintained 3rd party libraries are used.
* PostgreSQL everywhere
* 12Factor App for settings

Using this template
--------------------

.. code-block:: bash

    $ pip install cookiecutter
    $ cookiecutter https://github.com/sloria/cookiecutter-dj-project.git
    

"Your Stuff"
-------------

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.
