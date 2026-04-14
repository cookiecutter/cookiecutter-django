from pathlib import Path

from hooks.core.actions import DeleteDirectoryAction
from hooks.core.actions import DeleteFileAction
from hooks.core.context import ExecutionContext
from hooks.core.strategies import FeatureStrategy
from hooks.core.strategies import strategy


@strategy("rest_api", "Handle REST API configuration files")
class RestApiStrategy(FeatureStrategy):
    def should_apply(self, context: ExecutionContext) -> bool:
        return True

    def plan(self, context: ExecutionContext) -> list:
        actions = []
        rest_api = context.get_config("rest_api", "None")
        project_slug = context.project_slug

        if rest_api == "DRF":
            actions.extend(self._plan_drf(project_slug))
        elif rest_api == "Django Ninja":
            actions.extend(self._plan_ninja(project_slug))
        else:
            actions.extend(self._plan_no_api(project_slug))

        return actions

    def _plan_drf(self, project_slug: str) -> list:
        return [
            DeleteFileAction(
                file_path=Path("config", "api.py"),
                description="Remove Ninja API config (DRF mode)",
            ),
            DeleteFileAction(
                file_path=Path(project_slug, "users", "api", "schema.py"),
                description="Remove Ninja schema (DRF mode)",
            ),
        ]

    def _plan_ninja(self, project_slug: str) -> list:
        return [
            DeleteFileAction(
                file_path=Path("config", "api_router.py"),
                description="Remove DRF router (Ninja mode)",
            ),
            DeleteFileAction(
                file_path=Path(project_slug, "users", "api", "serializers.py"),
                description="Remove DRF serializers (Ninja mode)",
            ),
        ]

    def _plan_no_api(self, project_slug: str) -> list:
        return [
            DeleteFileAction(
                file_path=Path("config", "api_router.py"),
                description="Remove DRF router (no API)",
            ),
            DeleteFileAction(
                file_path=Path("config", "api.py"),
                description="Remove Ninja API config (no API)",
            ),
            DeleteFileAction(
                file_path=Path(project_slug, "users", "api", "serializers.py"),
                description="Remove DRF serializers (no API)",
            ),
            DeleteFileAction(
                file_path=Path(project_slug, "users", "api", "schema.py"),
                description="Remove Ninja schema (no API)",
            ),
            DeleteDirectoryAction(
                dir_path=Path(project_slug, "users", "api"),
                description="Remove API directory (no API)",
            ),
            DeleteDirectoryAction(
                dir_path=Path(project_slug, "users", "tests", "api"),
                description="Remove API tests directory (no API)",
            ),
        ]
