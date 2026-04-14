from pathlib import Path

from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("celery", "Handle Celery configuration files")
class CeleryStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return not context.is_enabled("use_celery")

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        project_slug = context.project_slug
        use_docker = context.is_enabled("use_docker")

        file_paths = [
            Path("config", "celery_app.py"),
            Path(project_slug, "users", "tasks.py"),
            Path(project_slug, "users", "tests", "test_tasks.py"),
        ]

        for file_path in file_paths:
            actions.append(
                DeleteFileAction(
                    file_path=file_path,
                    description=f"Remove Celery file: {file_path}",
                )
            )

        if use_docker:
            actions.extend(
                [
                    DeleteDirectoryAction(
                        dir_path=Path("compose", "local", "django", "celery"),
                        description="Remove local Celery Docker config",
                    ),
                    DeleteDirectoryAction(
                        dir_path=Path("compose", "production", "django", "celery"),
                        description="Remove production Celery Docker config",
                    ),
                ]
            )

        return actions
