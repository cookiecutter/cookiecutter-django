"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""

project_slug = '{{ cookiecutter.project_slug }}'
if hasattr(project_slug, 'isidentifier'):
    assert project_slug.isidentifier(), "'{}' project slug is not a valid Python identifier.".format(project_slug)

using_docker = '{{ cookiecutter.use_docker }}'.lower()
if using_docker == 'n':
    TERMINATOR = "\x1b[0m"
    WARNING = "\x1b[1;33m [WARNING]: "
    INFO = "\x1b[1;33m [INFO]: "
    HINT = "\x1b[3;33m"
    SUCCESS = "\x1b[1;32m [SUCCESS]: "

    import sys

    python_major_version = sys.version_info[0]
    if python_major_version == 2:
        sys.stdout.write(
            WARNING +
            "Cookiecutter Django does not support Python 2. "
            "Stability is guaranteed with Python 3.6+ only, "
            "are you sure you want to proceed (y/n)? " +
            TERMINATOR
        )
        yes_options, no_options = frozenset(['y']), frozenset(['n'])
        while True:
            choice = raw_input().lower()
            if choice in yes_options:
                break
            elif choice in no_options:
                sys.stdout.write(
                    INFO +
                    "Generation process stopped as requested." +
                    TERMINATOR
                )
                sys.exit(1)
            else:
                sys.stdout.write(
                    HINT +
                    "Please respond with {} or {}: ".format(
                        ', '.join(["'{}'".format(o) for o in yes_options if not o == '']),
                        ', '.join(["'{}'".format(o) for o in no_options if not o == ''])
                    ) +
                    TERMINATOR
                )

    sys.stdout.write(
        SUCCESS +
        "Project initialized, keep up the good work!" +
        TERMINATOR
    )
