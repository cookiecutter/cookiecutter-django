from __future__ import annotations

import random
import string
from pathlib import Path
from typing import Any

from hooks.core.actions import Action
from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.context import FailurePolicy
from hooks.core.executor import ActionExecutor
from hooks.core.strategies import FeatureStrategy
from hooks.strategies import AsyncStrategy
from hooks.strategies import CeleryStrategy
from hooks.strategies import CIToolStrategy
from hooks.strategies import DockerStrategy
from hooks.strategies import EditorStrategy
from hooks.strategies import FrontendPipelineStrategy
from hooks.strategies import HerokuStrategy
from hooks.strategies import OpenSourceLicenseStrategy
from hooks.strategies import RestApiStrategy
from hooks.strategies import UsernameTypeStrategy

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "
ERROR = "\x1b[1;31m [ERROR]: "

DEBUG_VALUE = "debug"

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


class ProjectGenerator:
    def __init__(
        self,
        config: dict[str, Any],
        dry_run: bool = False,
        failure_policy: FailurePolicy = FailurePolicy.STOP_IMMEDIATELY,
    ):
        self.config = config
        self.project_slug = config.get("project_slug", "project")
        self.context = ExecutionContext(
            project_slug=self.project_slug,
            cookiecutter_config=config,
            dry_run=dry_run,
            failure_policy=failure_policy,
        )
        self.executor = ActionExecutor(self.context)
        self._strategies: list[FeatureStrategy] = []

    def register_strategy(self, strategy: FeatureStrategy) -> None:
        self._strategies.append(strategy)

    def register_default_strategies(self) -> None:
        self._strategies = [
            OpenSourceLicenseStrategy(),
            UsernameTypeStrategy(),
            EditorStrategy(),
            DockerStrategy(),
            HerokuStrategy(),
            FrontendPipelineStrategy(),
            CeleryStrategy(),
            CIToolStrategy(),
            RestApiStrategy(),
            AsyncStrategy(),
        ]

    def plan(self) -> list[Action]:
        actions = []

        actions.extend(self._plan_secret_generation())
        actions.extend(self._plan_env_files())

        for strategy in self._strategies:
            if strategy.should_apply(self.context):
                strategy_actions = strategy.plan(self.context)
                actions.extend(strategy_actions)

        actions.extend(self._plan_dependencies())

        return actions

    def _plan_secret_generation(self) -> list[Action]:
        actions = []
        debug = self.context.is_enabled("debug")

        return actions

    def _plan_env_files(self) -> list[Action]:
        actions = []
        use_docker = self.context.is_enabled("use_docker")
        use_heroku = self.context.is_enabled("use_heroku")
        keep_local_envs = self.context.is_enabled("keep_local_envs_in_vcs")

        if not use_docker and not use_heroku:
            if not keep_local_envs:
                actions.extend(
                    [
                        DeleteDirectoryAction(
                            dir_path=Path(".envs"),
                            description="Remove .envs directory (no Docker/Heroku)",
                        ),
                        DeleteFileAction(
                            file_path=Path("merge_production_dotenvs_in_dotenv.py"),
                            description="Remove merge dotenvs script",
                        ),
                        DeleteDirectoryAction(
                            dir_path=Path("tests"),
                            description="Remove tests directory (no Docker/Heroku)",
                        ),
                    ],
                )

        return actions

    def _plan_dependencies(self) -> list[Action]:
        actions = []
        use_docker = self.context.is_enabled("use_docker")

        return actions

    def execute(self) -> bool:
        actions = self.plan()

        print(f"{INFO}Planning {len(actions)} actions for project generation...{TERMINATOR}")

        result = self.executor.execute(actions)

        if result.success:
            print(f"{SUCCESS}Project initialized, keep up the good work!{TERMINATOR}")
        else:
            print(f"{ERROR}Project generation failed: {result.message}{TERMINATOR}")
            if result.failed_actions:
                print(f"{ERROR}Failed actions: {', '.join(result.failed_actions)}{TERMINATOR}")

        report_path = Path(".generation_report.md")
        self.context.save_report(report_path)
        print(f"{INFO}Generation report saved to {report_path}{TERMINATOR}")

        return result.success

    def preview(self) -> str:
        actions = self.plan()
        lines = [f"Project Generation Preview for '{self.project_slug}'", "=" * 50, ""]

        for i, action in enumerate(actions, 1):
            lines.append(f"{i}. {action.describe()}")

        lines.extend(["", f"Total: {len(actions)} actions planned"])

        return "\n".join(lines)

    def get_report(self) -> str:
        return self.context.get_report()

    def get_json_report(self) -> dict[str, Any]:
        return self.context.get_json_report()


def generate_random_string(length, using_digits=False, using_ascii_letters=False, using_punctuation=False):
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    return DEBUG_VALUE if debug else generate_random_user()
