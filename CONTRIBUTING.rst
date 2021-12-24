How to Contribute
=================

Always happy to get issues identified and pull requests!

Getting your pull request merged in
------------------------------------

#. Keep it small. The smaller the pull request the more likely I'll pull it in.
#. Pull requests that fix a current issue get priority for review.

Testing
-------

Installation
~~~~~~~~~~~~

Please install `tox`_, which is a generic virtualenv management and test command line tool.

`tox`_ is available for download from `PyPI`_ via `pip`_::

    $ pip install tox

It will automatically create a fresh virtual environment and install our test dependencies,
such as `pytest-cookies`_ and `flake8`_.

Run the Tests
~~~~~~~~~~~~~

Tox uses py.test under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the `pytest usage docs`_.

To run all tests using various versions of python in virtualenvs defined in tox.ini, just run tox.::

    $ tox

It is possible to test with a specific version of python. To do this, the command
is::

    $ tox -e py39

This will run py.test with the python3.9 interpreter, for example.

To run a particular test with tox for against your current Python version::

    $ tox -e py -- -k test_default_configuration

.. _`pytest usage docs`: https://pytest.org/latest/usage.html#specifying-tests-selecting-tests
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`pytest-cookies`: https://pypi.python.org/pypi/pytest-cookies/
.. _`flake8`: https://pypi.python.org/pypi/flake8/
.. _`PyPI`: https://pypi.python.org/pypi
