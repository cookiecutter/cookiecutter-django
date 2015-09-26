Linters
=======

.. index:: linters


flake8
-------

To run flake8:

    $ flake8

The config for flake8 is located in setup.cfg. It specifies:

* Set max line length to 120 chars
* Exclude .tox,.git,*/migrations/*,*/static/CACHE/*,docs,node_modules
