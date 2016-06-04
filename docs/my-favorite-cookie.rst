************************************************
Creating your first app with Cookiecutter-Django
************************************************

This tutorial will show you how to build a simple app using the `Cookiecutter Django <https://github.com/pydanny/cookiecutter-django>`_ templating system. We'll be building a cookie polling app to determine the most popular flavor of cookie. 

Developers who have never used Django will learn the basics of creating a Django app; developers who are experienced with Django will learn how to set up a project within the Cookiecutter system. While many Django tutorials use the default SQLite database, Cookiecutter Django uses PostGres only, so we'll have you install and use that. 


Dependencies
============
This tutorial was written on Windows 10 using `git bash <https://git-for-windows.github.io/>`_; alternate instructions for Mac OS and Linux will be provided when needed. Any Linux-style shell should work for the following commands. 

You should have your preferred versions of `Python <https://www.python.org/downloads/>`_
and `Django <https://www.djangoproject.com/download/>`_ installed. Use the latest stable versions if you have no preference. 

You should have `Virtualenv <https://virtualenv.pypa.io/en/stable/>`_ and `Cookiecutter  <https://github.com/pydanny/cookiecutter-django/>`_ installed:

.. code-block:: python

    $ pip install virtualenv
    $ pip install cookiecutter

You should also have `PostgreSQL <https://www.postgresql.org/download/>`_ installed on your machine--just download and run the installer for your OS. The install menu will prompt you for a password, which you'll use when creating the project's database.


Instructions
============

1. **Setup** -- how to set up a virtual environment
2. **Cookiecutter** -- use Cookiecutter to initialize a project with your own customized information.
3. **Building the App** -- creating the My Favorite Cookie application.

============
1. Setup
============

Virtual Environment
"""""""""""""""""""

Create a virtual environment for your project. Cookiecutter will install a bunch of dependencies for you automatically; using a virtualenv will prevent this from interfering with your other work.

.. code-block:: python

    $ virtualenv c:/.virtualenvs/cookie_polls

Replace ``c:/.virtualenvs`` with the path to your own ``.virtualenvs`` folder.

Activate the virtual environment by calling ``source`` on the ``activate`` shell script . On Windows you'll call this from the virtualenv's ``scripts`` folder:

.. code-block:: python
    
    $  source /path/to/.virtualenvs/cookie_polls/scripts/activate

On other operating systems, it'll be found in the ``bin`` folder. 

.. code-block:: python
    
    $  source /path/to/.virtualenvs/cookie_polls/bin/activate

You'll know the virtual environment is active because its name will appear in parentheses before the command prompt. When you're done with this project, you can leave the virtual environment with the ``deactivate`` command. 

.. code-block:: python
    
    (cookie_polls)
    $  deactivate
  

Now you're ready to create your project using Cookiecutter. 


===============
2. Cookiecutter 
===============

Django developers may be familiar with the ``startproject`` command, which initializes the directory structure and required files for a bare-bones Django project. While this is fine when you're just learning Django for the first time, it's not great for a real production app. Cookiecutter takes care of a lot of standard tasks for you, including installing software dependencies, setting up testing files, and including and organizing common libraries like Bootstrap and AngularJS. It also generates a software license and a README.

Change directories into the folder where you want your project to live, and run ``cookiecutter`` followed by the URL of Cookiecutter's Github repo.

.. code-block:: python

    $ cd /my/project/folder
    (cookie_polls)
    my/project/folder  
    $ cookiecutter https://github.com/pydanny/cookiecutter-django

This will prompt you for a bunch of values specific to your project. Press "enter" without typing anything to use the default values, which are shown in [brackets] after the question. You can learn about all the different options `here, <http://cookiecutter-django.readthedocs.io/en/latest/project-generation-options.html>`_ but for now we'll use the defaults for everything but your name, your email, the project's name, and the project's description.

.. code-block:: python

     project_name [project_name]: My Favorite Cookie
     project_slug [My_Favorite_Cookie]: 
     author_name [Your Name]: Emily Cain
     email [Your email]: contact@emcain.net
     description [A short description of the project.]: Poll your friends to determine the most popular cookie. 

Then hit "enter" to use the default values for everything else. 

 

