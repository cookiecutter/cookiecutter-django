# Contributing to Cookicutter-Django-QuickStart

As an open source project, PackerShift welcomes contributions of many forms.

Examples of contributions include:

* Code patches
* Documentation improvements
* Bug reports and patch reviews

**Warning: non-trivial pull requests (anything more than fixing a typo) without
Trac tickets will be closed!** [Please file a ticket](https://github.com/packershift/cookiecutter-django-quickstart/issues/new/choose) to suggest changes.

Patches can be submitted as pull requests, but if you don't file a ticket, it's unlikely that we'll notice your contribution.

## How to Contribute

Always happy to get issues identified and pull requests!

## Getting your pull request merged in

1. Keep it small. The smaller the pull request, the more likely we are to accept.
2. Pull requests that fix a current issue get priority for review.

## Testing

### Installation

Please install [tox](https://tox.readthedocs.io/en/latest/), which is a generic virtualenv management and test command line tool.

[tox](https://tox.readthedocs.io/en/latest/) is available for download from [PyPI](https://pypi.python.org/pypi) via [pip](https://pypi.python.org/pypi/pip/):

```
pip install tox
```

It will automatically create a fresh virtual environment and install our test dependencies,
such as [pytest-cookies](https://pypi.python.org/pypi/pytest-cookies/) and [flake8](https://pypi.python.org/pypi/flake8/).

### Run the Tests

Tox uses pytest under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the [pytest usage docs](https://pytest.org/latest/usage.html#specifying-tests-selecting-tests).

To run all tests using various versions of python in virtualenvs defined in tox.ini, just run tox.:

```python
tox
```

It is possible to test with a specific version of python. To do this, the command
is:

```
tox -e py310
```

This will run pytest with the python3.10 interpreter, for example.

To run a particular test with tox for against your current Python version:

```
tox -e py -- -k test_default_configuration
```

## Code of Conduct

As a contributor, you can help us keep the Django community open and inclusive. Please read and follow our [Code of Conduct](<https://github.com/packershift/.github/blob/main/CODE_OF_CONDUCT.md>).
