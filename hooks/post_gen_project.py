"""
Post-generation hook for cookiecutter-django.

This module has been refactored to use a modern, modular architecture:

1. Operation Abstraction (operations.py)
   - All file operations are defined as data objects
   - Separation of "what to do" from "how to do it"

2. Audit Trail (audit.py)
   - Every operation is recorded
   - Change report generation
   - Rollback support

3. Executor (executor.py)
   - Multiple execution modes: real, dry-run, log-only
   - Two-phase execution: decision phase + execution phase
   - Error recovery with automatic rollback

4. Strategy Pattern (strategies.py)
   - Each feature option is a strategy class
   - No if/else branches in main flow
   - Strategies declare what files to delete/modify

5. Configuration Generators (config_generators.py)
   - Pure functions for generating secrets and configs
   - Separated from file operations
"""

import sys

from hooks.config_generators import SecretConfig
from hooks.config_generators import create_dependency_operations
from hooks.config_generators import create_flag_operations
from hooks.config_generators import get_warning_messages
from hooks.executor import ExecutionMode
from hooks.executor import TwoPhaseExecutor

# Import our new modules
from hooks.strategies import ProjectContext
from hooks.strategies import registry

# Color constants for terminal output
TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def main() -> None:
    """
    Main entry point for post-generation processing.

    The flow is:
    1. Create project context from cookiecutter variables
    2. Phase 1 (Decision): Collect all operations in memory
    3. Optional: Preview operations
    4. Phase 2 (Execution): Execute all operations with audit trail
    5. Generate and print change report
    """
    # Create project context from cookiecutter variables
    context = ProjectContext.from_cookiecutter()
    debug = context.is_yes(context.debug)

    # Initialize the two-phase executor
    executor = TwoPhaseExecutor()

    # ========================================================================
    # PHASE 1: Decision Phase - Collect all operations in memory
    # ========================================================================

    # 1. Generate and set secrets/flags
    secret_config = SecretConfig.generate(debug=debug)
    flag_operations = create_flag_operations(secret_config)
    executor.add_operations(flag_operations)

    # 2. Collect operations from all applicable strategies
    strategy_operations = registry.collect_operations(context)
    executor.add_operations(strategy_operations)

    # 3. Dependency installation operations
    dependency_operations = create_dependency_operations(
        use_docker=context.is_yes(context.use_docker),
    )
    executor.add_operations(dependency_operations)

    # ========================================================================
    # Optional: Preview phase - Show what will be done
    # ========================================================================

    # Uncomment the following line to enable preview mode:
    # executor.print_preview()
    # response = input("\nContinue? [y/N]: ")
    # if response.lower() != 'y':
    #     print("Aborted.")
    #     return

    # ========================================================================
    # PHASE 2: Execution Phase - Execute all operations
    # ========================================================================

    print("\nInitializing project...")

    try:
        # Execute in real mode with auto-rollback on failure
        audit_log = executor.execute(
            mode=ExecutionMode.REAL,
            auto_rollback=True,
            confirm=False,  # Set to True for interactive confirmation
        )

        # Print change report
        audit_log.print_report()

    except Exception as e:
        print(f"\n{WARNING}Error during project initialization: {e}{TERMINATOR}")
        sys.exit(1)

    # ========================================================================
    # Print warnings
    # ========================================================================

    # Convert context to dict for warning generator
    context_dict = {
        "use_docker": context.use_docker,
        "use_heroku": context.use_heroku,
        "cloud_provider": context.cloud_provider,
        "keep_local_envs_in_vcs": context.keep_local_envs_in_vcs,
    }

    warnings = get_warning_messages(context_dict)
    for warning in warnings:
        print(f"{WARNING}{warning}{TERMINATOR}")

    print(f"{SUCCESS}Project initialized, keep up the good work!{TERMINATOR}")


if __name__ == "__main__":
    main()
