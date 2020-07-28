.. _document:

Document
=========

This project uses Sphinx_ documentation generator.

After you have set up to `develop locally`_, run the following command from the project directory to build and serve HTML documentation: ::

    $ make -C docs livehtml

If you set up your project to `develop locally with docker`_, run the following command: ::

    $ docker-compose -f local.yml up docs

Navigate to port 7000 on your host to see the documentation. This will be opened automatically at `localhost`_ for local, non-docker development.

Generate API documentation
----------------------------

Edit the ``docs/_source`` files and project application docstrings to create your documentation.

Sphinx can automatically include class and function signatures and docstrings in generated documentation. 
See the generated project documentation for more examples.

.. _localhost: http://localhost:7000/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _develop locally: ./developing-locally.html
.. _develop locally with docker: ./developing-locally-docker.html
