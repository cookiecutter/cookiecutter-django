.. _document:

Document
=========

This project uses Sphinx_ documentation generator.

After you have set up to `develop locally`_, run the following command from the project directory to build and serve HTML documentation: ::

    $ make -C docs livehtml

If you set up your project to `develop locally with docker`_, run the following command: ::

    $ docker compose -f docker-compose.docs.yml up

Navigate to port 9000 on your host to see the documentation. This will be opened automatically at `localhost`_ for local, non-docker development.

Note: using Docker for documentation sets up a temporary SQLite file by setting the environment variable ``DATABASE_URL=sqlite:///readthedocs.db`` in ``docs/conf.py`` to avoid a dependency on PostgreSQL.

Generate API documentation
----------------------------

Edit the ``docs`` files and project application docstrings to create your documentation.

Sphinx can automatically include class and function signatures and docstrings in generated documentation.
See the generated project documentation for more examples.

Setting up ReadTheDocs
----------------------

To setup your documentation on `ReadTheDocs`_, you must

1. Go to `ReadTheDocs`_ and login/create an account
2. Add your GitHub repository
3. Trigger a build

Additionally, you can auto-build Pull Request previews, but `you must enable it`_.

.. _localhost: http://localhost:9000/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _develop locally: ./developing-locally.html
.. _develop locally with docker: ./developing-locally-docker.html
.. _ReadTheDocs: https://readthedocs.org/
.. _you must enable it: https://docs.readthedocs.io/en/latest/guides/autobuild-docs-for-pull-requests.html#autobuild-documentation-for-pull-requests
