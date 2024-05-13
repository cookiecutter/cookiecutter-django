Linters
=======

.. index:: linters


ruff
------

Ruff is a Python linter and code formatter, written in Rust.
It is a aggregation of flake8, pylint, pyupgrade and many more.

Ruff comes with a linter (``ruff check``) and a formatter (``ruff format``).
The linter is a wrapper around flake8, pylint, and other linters,
and the formatter is a wrapper around black, isort, and other formatters.

To run ruff without modifying your files: ::

    $ ruff format --diff .
    $ ruff check .

Ruff is capable of fixing most of the problems it encounters.
Be sure you commit first before running `ruff` so you can restore to a savepoint (and amend afterwards to prevent a double commit. : ::

    $ ruff format  .
    $ ruff check --fix .
    # be careful with the --unsafe-fixes option, it can break your code
    $ ruff check --fix --unsafe-fixes  .

The config for ruff is located in pyproject.toml.
On of the most important option is `tool.ruff.lint.select`.
`select` determines which linters are run. In example, `DJ <https://docs.astral.sh/ruff/rules/#flake8-django-dj>`_ refers to flake8-django.
For a full list of available linters, see `https://docs.astral.sh/ruff/rules/ <https://docs.astral.sh/ruff/rules/>`_
