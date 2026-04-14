from __future__ import annotations

import sys
from pathlib import Path

from hooks.core import (
    DEBUG_VALUE,
    INFO,
    SUCCESS,
    TERMINATOR,
    WARNING,
    ExecutionContext,
    FailureStrategy,
    generate_random_string,
    generate_random_user,
)
from hooks.strategies import ALL_STRATEGIES


def get_cookiecutter_context() -> dict:
    return {
        "open_source_license": "{{ cookiecutter.open_source_license }}",
        "username_type": "{{ cookiecutter.username_type }}",
        "editor": "{{ cookiecutter.editor }}",
        "use_docker": "{{ cookiecutter.use_docker }}",
        "cloud_provider": "{{ cookiecutter.cloud_provider }}",
        "use_heroku": "{{ cookiecutter.use_heroku }}",
        "ci_tool": "{{ cookiecutter.ci_tool }}",
        "keep_local_envs_in_vcs": "{{ cookiecutter.keep_local_envs_in_vcs }}",
        "frontend_pipeline": "{{ cookiecutter.frontend_pipeline }}",
        "use_celery": "{{ cookiecutter.use_celery }}",
        "rest_api": "{{ cookiecutter.rest_api }}",
        "use_async": "{{ cookiecutter.use_async }}",
        "debug": "{{ cookiecutter.debug }}",
    }


def main() -> None:
    context = get_cookiecutter_context()
    debug = context["debug"].lower() == "y"

    if (
        context["cloud_provider"] == "None"
        and context["use_docker"].lower() == "n"
    ):
        print(
            WARNING + "You chose to not use any cloud providers nor Docker, "
            "media files won't be served in production." + TERMINATOR,
        )

    execution_context = ExecutionContext(
        failure_strategy=FailureStrategy.ROLLBACK,
        dry_run=False,
    )

    print("Phase 1: Collecting operations from strategies...")
    for strategy_class in ALL_STRATEGIES:
        strategy = strategy_class()
        if strategy.should_apply(context):
            operations = strategy.collect_operations(context)
            for op in operations:
                execution_context.add_operation(op)

    print(f"Collected {len(execution_context.operations)} operations to execute.")
    if debug:
        print("\nOperations preview:")
        for i, op in enumerate(execution_context.operations, 1):
            print(f"  {i}. [{op.operation_type.value}] {op.target}")
        print()

    print("Phase 2: Executing all operations...")
    try:
        execution_context.execute_all()
    except Exception as e:
        print(f"Fatal error during execution: {e}", file=sys.stderr)
        sys.exit(1)

    execution_context.print_report()
    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


def append_to_gitignore_file(ignored_line: str) -> None:
    with Path(".gitignore").open("a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


if __name__ == "__main__":
    main()
