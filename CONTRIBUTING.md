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

This last step is very important, don't start developing from main, it'll cause pain if you need to send another change later.

> [!TIP]
> This repository includes a `.github/copilot-instructions.md` file. If you use GitHub Copilot, these instructions will help the AI understand the Cookiecutter template syntax and provide more accurate code suggestions.

## Testing

You'll need to run the tests using Python 3.13. We recommend using [tox](https://tox.readthedocs.io/en/latest/) to run the tests. It will automatically create a fresh virtual environment and install our test dependencies, such as [pytest-cookies](https://pypi.python.org/pypi/pytest-cookies/) and [flake8](https://pypi.python.org/pypi/flake8/).

We'll also run the tests on GitHub actions when you send your pull request, but it's a good idea to run them locally before you send it.

### Installation

We use uv to manage our environment and manage our Python installation. You can install it following the instructions at https://docs.astral.sh/uv/getting-started/installation/

### Run the template's test suite

To run the tests of the template using the current Python version:

```bash
$ uv run tox run -e py