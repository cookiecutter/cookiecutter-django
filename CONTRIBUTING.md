# How to Contribute

Always happy to get issues identified and pull requests!

## Getting your pull request merged in

1.  Keep it small. The smaller the pull request, the more likely we are to accept.
2.  Pull requests that fix a current issue get priority for review.

## Testing

### Installation

Please install [tox](https://tox.readthedocs.io/en/latest/), which is a generic virtualenv management and test command line tool.

[tox](https://tox.readthedocs.io/en/latest/) is available for download from [PyPI](https://pypi.python.org/pypi) via [pip](https://pypi.python.org/pypi/pip/):

    $ pip install tox

It will automatically create a fresh virtual environment and install our test dependencies,
such as [pytest-cookies](https://pypi.python.org/pypi/pytest-cookies/) and [flake8](https://pypi.python.org/pypi/flake8/).

### Run the Tests

Tox uses pytest under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the [pytest usage docs](https://pytest.org/latest/usage.html#specifying-tests-selecting-tests).

To run all tests using various versions of python in virtualenvs defined in tox.ini, just run tox.:

    $ tox

It is possible to test with a specific version of python. To do this, the command
is:

    $ tox -e py310

This will run pytest with the python3.10 interpreter, for example.

To run a particular test with tox for against your current Python version:

    $ tox -e py -- -k test_default_configuration
