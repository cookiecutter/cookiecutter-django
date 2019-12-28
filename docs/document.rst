.. _document:

Document
=========

This project uses Sphinx_ documentation generator.
After you have set up to `develop locally`_, run the following commands to generate the HTML documentation: ::

    $ sphinx-build docs/ docs/_build/html/

If you set up your project to `develop locally with docker`_, run the following command: ::

    $ docker-compose -f local.yml run --rm django sphinx-build docs/ docs/_build/html/

Generate API documentation
----------------------------

Sphinx can automatically generate documentation from docstrings, to enable this feature, follow these steps:

1. Add Sphinx extension in ``docs/conf.py`` file, like below: ::

    extensions = [
        'sphinx.ext.autodoc',
    ]

2. Uncomment the following lines in the ``docs/conf.py`` file: ::

    # import django
    # sys.path.insert(0, os.path.abspath('..'))
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    # django.setup()

3. Run the following command: ::

    $ sphinx-apidoc -f -o ./docs/modules/ ./tpub/ migrations/*

   If you set up your project to `develop locally with docker`_, run the following command: ::

    $ docker-compose -f local.yml run --rm django sphinx-apidoc -f -o ./docs/modules ./tpub/ migrations/*

4. Regenerate HTML documentation as written above.

.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _develop locally: ../developing-locally.rst
.. _develop locally with docker: ..../developing-locally-docker.rst
