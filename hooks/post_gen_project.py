# ruff: noqa: PLR0133
import os
import random
import shutil
import string
import subprocess
import sys
from pathlib import Path

from hooks.core.actions import AppendFileAction
from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.actions import ModifyFileAction
from hooks.core.context import ExecutionContext
from hooks.core.context import FailurePolicy
from hooks.core.executor import ActionExecutor
from hooks.core.strategies import FeatureStrategy
from hooks.strategies.async_strategy import AsyncStrategy
from hooks.strategies.celery import CeleryStrategy
from hooks.strategies.ci_tool import CIToolStrategy
from hooks.strategies.docker import DockerStrategy
from hooks.strategies.editor import EditorStrategy
from hooks.strategies.frontend_pipeline import FrontendPipelineStrategy
from hooks.strategies.heroku import HerokuStrategy
from hooks.strategies.license import OpenSourceLicenseStrategy
from hooks.strategies.rest_api import RestApiStrategy
from hooks.strategies.username_type import UsernameTypeStrategy

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "
ERROR = "\x1b[1;31m [ERROR]: "

DEBUG_VALUE = "debug"


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


class SecretGenerationStrategy(FeatureStrategy):
    name = "secrets"
    description = "Generate secret keys and credentials"

    def __init__(self, debug=False):
        self.debug = debug
        self.postgres_user = DEBUG_VALUE if debug else generate_random_user()
        self.celery_flower_user = DEBUG_VALUE if debug else generate_random_user()

    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        from hooks.core.actions import ModifyFileAction

        actions = []

        actions.extend(self._plan_env_secrets())
        actions.extend(self._plan_settings_secrets())

        return actions

    def _plan_env_secrets(self) -> list:
        actions = []

        local_django_envs_path = Path(".envs", ".local", ".django")
        production_django_envs_path = Path(".envs", ".production", ".django")
        local_postgres_envs_path = Path(".envs", ".local", ".postgres")
        production_postgres_envs_path = Path(".envs", ".production", ".postgres")

        actions.append(
            ModifyFileAction(
                file_path=production_django_envs_path,
                modifications={"!!!SET DJANGO_SECRET_KEY!!!": self._generate_secret_key()},
                description="Set Django secret key in production env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=production_django_envs_path,
                modifications={"!!!SET DJANGO_ADMIN_URL!!!": self._generate_admin_url()},
                description="Set Django admin URL in production env",
            )
        )

        postgres_password = DEBUG_VALUE if self.debug else self._generate_password()
        actions.append(
            ModifyFileAction(
                file_path=local_postgres_envs_path,
                modifications={"!!!SET POSTGRES_USER!!!": self.postgres_user},
                description="Set Postgres user in local env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=local_postgres_envs_path,
                modifications={"!!!SET POSTGRES_PASSWORD!!!": postgres_password},
                description="Set Postgres password in local env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=production_postgres_envs_path,
                modifications={"!!!SET POSTGRES_USER!!!": self.postgres_user},
                description="Set Postgres user in production env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=production_postgres_envs_path,
                modifications={"!!!SET POSTGRES_PASSWORD!!!": postgres_password},
                description="Set Postgres password in production env",
            )
        )

        celery_flower_password = DEBUG_VALUE if self.debug else self._generate_password()
        actions.append(
            ModifyFileAction(
                file_path=local_django_envs_path,
                modifications={"!!!SET CELERY_FLOWER_USER!!!": self.celery_flower_user},
                description="Set Celery Flower user in local env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=local_django_envs_path,
                modifications={"!!!SET CELERY_FLOWER_PASSWORD!!!": celery_flower_password},
                description="Set Celery Flower password in local env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=production_django_envs_path,
                modifications={"!!!SET CELERY_FLOWER_USER!!!": self.celery_flower_user},
                description="Set Celery Flower user in production env",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=production_django_envs_path,
                modifications={"!!!SET CELERY_FLOWER_PASSWORD!!!": celery_flower_password},
                description="Set Celery Flower password in production env",
            )
        )

        return actions

    def _plan_settings_secrets(self) -> list:
        actions = []

        local_settings_path = Path("config", "settings", "local.py")
        test_settings_path = Path("config", "settings", "test.py")

        actions.append(
            ModifyFileAction(
                file_path=local_settings_path,
                modifications={"!!!SET DJANGO_SECRET_KEY!!!": self._generate_secret_key()},
                description="Set Django secret key in local settings",
            )
        )
        actions.append(
            ModifyFileAction(
                file_path=test_settings_path,
                modifications={"!!!SET DJANGO_SECRET_KEY!!!": self._generate_secret_key()},
                description="Set Django secret key in test settings",
            )
        )

        return actions

    def _generate_secret_key(self) -> str:
        key = generate_random_string(64, using_digits=True, using_ascii_letters=True)
        return key if key else "!!!SET DJANGO_SECRET_KEY!!!"

    def _generate_admin_url(self) -> str:
        key = generate_random_string(32, using_digits=True, using_ascii_letters=True)
        return f"{key}/" if key else "!!!SET DJANGO_ADMIN_URL!!!/"

    def _generate_password(self) -> str:
        key = generate_random_string(64, using_digits=True, using_ascii_letters=True)
        return key if key else "!!!SET PASSWORD!!!"


class EnvFilesStrategy(FeatureStrategy):
    name = "env_files"
    description = "Handle .env files configuration"

    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        use_docker = context.is_enabled("use_docker")
        use_heroku = context.is_enabled("use_heroku")
        keep_local_envs = context.is_enabled("keep_local_envs_in_vcs")

        if not use_docker and not use_heroku:
            if not keep_local_envs:
                actions.append(
                    DeleteDirectoryAction(
                        dir_path=Path(".envs"),
                        description="Remove .envs directory (no Docker/Heroku)",
                    )
                )
                actions.append(
                    DeleteFileAction(
                        file_path=Path("merge_production_dotenvs_in_dotenv.py"),
                        description="Remove merge dotenvs script",
                    )
                )
                actions.append(
                    DeleteDirectoryAction(
                        dir_path=Path("tests"),
                        description="Remove tests directory (no Docker/Heroku)",
                    )
                )

        return actions


class GitignoreStrategy(FeatureStrategy):
    name = "gitignore"
    description = "Update .gitignore file"

    def should_apply(self, context: ExecutionContext) -> bool:
        use_docker = context.is_enabled("use_docker")
        use_heroku = context.is_enabled("use_heroku")
        return use_docker or use_heroku

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        keep_local_envs = context.is_enabled("keep_local_envs_in_vcs")

        actions.append(
            AppendFileAction(
                file_path=Path(".gitignore"),
                content=".env",
                description="Add .env to gitignore",
            )
        )
        actions.append(
            AppendFileAction(
                file_path=Path(".gitignore"),
                content=".envs/*",
                description="Add .envs/* to gitignore",
            )
        )

        if keep_local_envs:
            actions.append(
                AppendFileAction(
                    file_path=Path(".gitignore"),
                    content="!.envs/.local/",
                    description="Keep local envs in VCS",
                )
            )

        return actions


class DependenciesStrategy(FeatureStrategy):
    name = "dependencies"
    description = "Install project dependencies"

    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        from hooks.core.actions import RunCommandAction

        actions = []
        use_docker = context.is_enabled("use_docker")

        if use_docker:
            uv_docker_image_path = Path("compose/local/uv/Dockerfile")
            uv_image_tag = "cookiecutter-django-uv-runner:latest"

            actions.append(
                RunCommandAction(
                    command=[
                        "docker",
                        "build",
                        "--load",
                        "-t",
                        uv_image_tag,
                        "-f",
                        str(uv_docker_image_path),
                        "-q",
                        ".",
                    ],
                    description="Build uv Docker image",
                    env={"DOCKER_BUILDKIT": "1"},
                )
            )

            current_path = Path.cwd().absolute()
            uv_cmd = ["docker", "run", "--rm", "-v", f"{current_path}:/app", uv_image_tag, "uv"]
        else:
            uv_cmd = ["uv"]

        actions.append(
            RunCommandAction(
                command=[*uv_cmd, "add", "--no-sync", "-r", "requirements/production.txt"],
                description="Install production dependencies",
            )
        )

        actions.append(
            RunCommandAction(
                command=[*uv_cmd, "add", "--no-sync", "--dev", "-r", "requirements/local.txt"],
                description="Install development dependencies",
            )
        )

        actions.append(
            DeleteDirectoryAction(
                dir_path=Path("requirements"),
                description="Remove requirements directory",
            )
        )

        uv_image_parent_dir_path = Path("compose/local/uv")
        if uv_image_parent_dir_path.exists():
            actions.append(
                DeleteDirectoryAction(
                    dir_path=uv_image_parent_dir_path,
                    description="Remove uv Docker image directory",
                )
            )

        return actions


class ProjectGenerationOrchestrator:
    def __init__(self, config: dict, dry_run: bool = False, failure_policy: FailurePolicy = FailurePolicy.STOP_IMMEDIATELY):
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
        self.debug = config.get("debug", "n").lower() == "y"

    def register_strategy(self, strategy: FeatureStrategy) -> None:
        self._strategies.append(strategy)

    def register_all_strategies(self) -> None:
        self._strategies = [
            SecretGenerationStrategy(debug=self.debug),
            OpenSourceLicenseStrategy(),
            UsernameTypeStrategy(),
            EditorStrategy(),
            DockerStrategy(),
            HerokuStrategy(),
            EnvFilesStrategy(),
            GitignoreStrategy(),
            FrontendPipelineStrategy(),
            CeleryStrategy(),
            CIToolStrategy(),
            RestApiStrategy(),
            AsyncStrategy(),
            DependenciesStrategy(),
        ]

    def plan(self) -> list:
        actions = []

        for strategy in self._strategies:
            if strategy.should_apply(self.context):
                strategy_actions = strategy.plan(self.context)
                actions.extend(strategy_actions)

        return actions

    def execute(self) -> bool:
        print(f"{INFO}Planning project generation...{TERMINATOR}")
        actions = self.plan()

        print(f"{INFO}Found {len(actions)} actions to execute{TERMINATOR}")

        if self.context.dry_run:
            print(f"{INFO}Dry-run mode: showing planned actions{TERMINATOR}")
            for i, action in enumerate(actions, 1):
                print(f"  [{i}/{len(actions)}] {action.describe()}")
            return True

        result = self.executor.execute(actions)

        if result.success:
            print(f"{SUCCESS}Project initialized, keep up the good work!{TERMINATOR}")
        else:
            print(f"{ERROR}Project generation failed: {result.message}{TERMINATOR}")
            if result.failed_actions:
                print(f"{ERROR}Failed actions: {', '.join(result.failed_actions)}{TERMINATOR}")
            if result.rolled_back_count > 0:
                print(f"{INFO}Rolled back {result.rolled_back_count} actions{TERMINATOR}")

        report_path = Path(".generation_report.md")
        self.context.save_report(report_path)
        print(f"{INFO}Generation report saved to {report_path}{TERMINATOR}")

        json_report_path = Path(".generation_report.json")
        self.context.save_json_report(json_report_path)
        print(f"{INFO}JSON report saved to {json_report_path}{TERMINATOR}")

        return result.success

    def preview(self) -> str:
        actions = self.plan()
        lines = [f"Project Generation Preview for '{self.project_slug}'", "=" * 50, ""]

        for i, action in enumerate(actions, 1):
            lines.append(f"{i}. {action.describe()}")

        lines.extend(["", f"Total: {len(actions)} actions planned"])

        return "\n".join(lines)


def print_warning(message: str) -> None:
    print(f"{WARNING}{message}{TERMINATOR}")


def main():
    config = {
        "project_slug": "{{ cookiecutter.project_slug }}",
        "open_source_license": "{{ cookiecutter.open_source_license }}",
        "username_type": "{{ cookiecutter.username_type }}",
        "editor": "{{ cookiecutter.editor }}",
        "use_docker": "{{ cookiecutter.use_docker }}",
        "cloud_provider": "{{ cookiecutter.cloud_provider }}",
        "use_heroku": "{{ cookiecutter.use_heroku }}",
        "frontend_pipeline": "{{ cookiecutter.frontend_pipeline }}",
        "use_celery": "{{ cookiecutter.use_celery }}",
        "ci_tool": "{{ cookiecutter.ci_tool }}",
        "rest_api": "{{ cookiecutter.rest_api }}",
        "use_async": "{{ cookiecutter.use_async }}",
        "keep_local_envs_in_vcs": "{{ cookiecutter.keep_local_envs_in_vcs }}",
        "debug": "{{ cookiecutter.debug }}",
    }

    orchestrator = ProjectGenerationOrchestrator(config)
    orchestrator.register_all_strategies()

    cloud_provider = config.get("cloud_provider", "None")
    use_docker = config.get("use_docker", "n").lower() == "y"

    if cloud_provider == "None" and not use_docker:
        print_warning(
            "You chose to not use any cloud providers nor Docker, "
            "media files won't be served in production."
        )

    use_docker_config = config.get("use_docker", "n").lower() == "y"
    use_heroku_config = config.get("use_heroku", "n").lower() == "y"
    keep_local_envs = config.get("keep_local_envs_in_vcs", "y").lower() == "y"

    if not use_docker_config and not use_heroku_config and keep_local_envs:
        print_warning(
            ".env(s) are only utilized when Docker Compose and/or "
            "Heroku support is enabled. Keeping them as requested, but they may not be useful "
            "in your current setup."
        )

    success = orchestrator.execute()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
