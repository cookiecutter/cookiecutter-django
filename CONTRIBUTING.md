# How to Contribute

Always happy to get issues identified and pull requests!

## General considerations

1. Keep it small. The smaller the change, the more likely we are to accept.
2. Changes that fix a current issue get priority for review.
3. Check out [GitHub guide][submit-a-pr] if you've never created a pull request before.

## Getting started

1. Fork the repo
2. Clone your fork
3. Create a branch for your changes

This last step is very important, don't start developing from master, it'll cause pain if you need to send another change later.

## Testing

You'll need to run the tests using Python 3.11. We recommend using [tox](https://tox.readthedocs.io/en/latest/) to run the tests. It will automatically create a fresh virtual environment and install our test dependencies, such as [pytest-cookies](https://pypi.python.org/pypi/pytest-cookies/) and [flake8](https://pypi.python.org/pypi/flake8/).

We'll also run the tests on GitHub actions when you send your pull request, but it's a good idea to run them locally before you send it.

### Installation

First, make sure that your version of Python is 3.11:

```bash
$ python --version
Python 3.11.3
```

Any version that starts with 3.11 will do. If you need to install it, you can get it from [python.org](https://www.python.org/downloads/).

Then install `tox`, if not already installed:

```bash
$ python -m pip install tox
```

### Run the template's test suite

To run the tests of the template using the current Python version:

```bash
$ tox -e py
```

This uses `pytest `under the hood, and you can pass options to it after a `--`. So to run a particular test:

```bash
$ tox -e py -- -k test_default_configuration
```

For further information, please consult the [pytest usage docs](https://pytest.org/en/latest/how-to/usage.html#specifying-which-tests-to-run).

### Run the generated project tests

The template tests are checking that the generated project is fully rendered and that it passes `flake8`. We also have some test scripts which generate a specific project combination, install the dependencies, run the tests of the generated project, install FE dependencies and generate the docs. They will install the template dependencies, so make sure you create and activate a virtual environment first.

```bash
$ python -m venv venv
$ source venv/bin/activate
```

These tests are slower and can be run with or without Docker:

- Without Docker: `scripts/test_bare.sh` (for bare metal)
- With Docker: `scripts/test_docker.sh`

All arguments to these scripts will be passed to the `cookiecutter` CLI, letting you set options, for example:

```bash
$ scripts/test_bare.sh use_celery=y
```

## Submitting a pull request

Once you're happy with your changes and they look ok locally, push and send send [a pull request][submit-a-pr] to the main repo, which will trigger the tests on GitHub actions. If they fail, try to fix them. A maintainer should take a look at your change and give you feedback or merge it.

[submit-a-pr]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
