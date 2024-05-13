.. {{ cookiecutter.project_name }} documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howto{% if cookiecutter.editor == 'PyCharm' %}
   pycharm/configuration{% endif %}
   users



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
